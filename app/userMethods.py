from models import UserModel
class UserMethods:
    @staticmethod
    #add a type checking for clerk_user_id
    async def User_Exists(db: AsyncSession,clerk_user_id) -> bool:
        user = await db.get(UserModel, clerk_user_id)
        if user is None:
            return False
        else: 
            return True