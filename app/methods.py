from models import UserModel,SessionModel
from database import AsyncSession
from schemas import AuthUser
from uuid6 import uuid7
class UserMethods:
    #! first two  function will not be used 
    @staticmethod
    async def get_or_create_user(
        db: AsyncSession, clerk_user: AuthUser
    ) -> UserModel:
        db_user = UserModel(
            user_id=uuid7(),
            email=clerk_user.email,
            clerk_id=clerk_user.clerk_user_id,
        )
        db.add(db_user)

        try:
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except IntegrityError:
            await db.rollback()
            # User already exists! Fetch and return the existing record
            stmt = select(UserModel).where(
                UserModel.clerk_id == clerk_user.clerk_user_id
            )
            result = await db.execute(stmt)
            return result.scalar_one()
class SessionMethods:
    #fetches chat history and id's
    @staticmethod
    async def get(db : AsyncSession,session_id) -> SessionModel:
        session=await db.get(SessionModel, session_id)
        return session
    @staticmethod
    async def save_or_update(
        db: AsyncSession, 
        session_query: SessionQuery, 
        full_llm_response: str
    ) -> SessionModel:
        # Build updated conversation (existing history + new AI message)
        updated_history = session_query.chat_history.model_dump()
        updated_history["conversation"].append({
            "role": "assistant",
            "content": full_llm_response
        })

        # Fetch existing record
        stmt = select(SessionModel).where(SessionModel.session_id == session_query.session_id)
        result = await db.execute(stmt)
        session_record = result.scalar_one_or_none()

        if session_record:
            # 🔒 Integrity Check 1: Verify Ownership
            if session_record.session_user_id != session_query.session_user_id:
                logger.error(
                    "User ID mismatch on session update", 
                    session_id=str(session_query.session_id),
                    owner_id=str(session_record.session_user_id),
                    requester_id=str(session_query.session_user_id)
                )
                raise PermissionError("User does not have permission to modify this session.")

            # Update existing session & flag JSON modification
            session_record.chat_history = updated_history
            flag_modified(session_record, "chat_history")
        else:
            # Create new session
            session_record = SessionModel(
                session_id=session_query.session_id,
                session_user_id=session_query.session_user_id,
                chat_history=updated_history
            )
            db.add(session_record)

        # 🔒 Integrity Check 2: Database Constraints
        try:
            await db.commit()
            await db.refresh(session_record)
            return session_record
            
        except IntegrityError as e:
            await db.rollback()
            logger.error(
                "Database integrity error during session save_or_update", 
                session_id=str(session_query.session_id),
                error=str(e)
            )
            raise ValueError("Failed to persist session due to database constraint violation.") from e