from models import UserModel
from database import AsyncSession
from schemas import AuthUser
from uuid6 import uuid7
print(uuid7())
class UserMethods:
    #! first two  function will not be used 
    """
    @staticmethod
    #add a type checking for clerk_user_id
    async def userExists(db: AsyncSession,clerk_user: AuthUser) -> bool:
        stmt = select(UserModel).where(
            UserModel.clerk_id == clerk_user.clerk_user_id
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user is not None
    @staticmethod
    async def post_user(db: AsyncSession,clerk_user: AuthUser)-> UserModel:
        db_user=UserModel(
            user_id=uuid7(),
            email=clerk_user.email,
            clerk_id=clerk_user.clerk_user_id)
        db.add(db_user)
        try:
            await db.commit()
            await db.refresh(db_user)
            return db_user 
        except Exception as e:
            await db.rollback()
            #TODO in future add here an exception using structlogger
            print(f"error {e}")
            raise
    """
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