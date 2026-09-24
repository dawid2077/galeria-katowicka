from from
async def get_valid_user_session(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(auth_user)
) -> SessionModel:
    session = await SessionMethods.get(db, session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    if session.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    return session