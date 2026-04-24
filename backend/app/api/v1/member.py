"""Member API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.member import Member
from app.services.wechat import code2session
from app.middleware.auth import create_token, get_current_member_id
from app.utils.response import success, error, ERR_BAD_REQUEST, ERR_NOT_FOUND, ERR_UNAUTHORIZED, ERR_INTERNAL
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class LoginRequest(BaseModel):
    code: str


class UpdateMemberRequest(BaseModel):
    nickname: str | None = None
    avatar_url: str | None = None
    phone: str | None = None


@router.post("/login")
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    """微信授权登录"""
    try:
        wechat_data = await code2session(body.code)
    except Exception as e:
        return error(ERR_BAD_REQUEST, f"微信登录失败: {str(e)}")
    
    open_id = wechat_data.get("open_id")
    session_key = wechat_data.get("session_key")
    
    if not open_id:
        return error(ERR_BAD_REQUEST, "微信登录失败: 未获取到openid")
    
    # Find or create member
    member_obj = db.query(Member).filter(Member.open_id == open_id).first()
    if not member_obj:
        member_obj = Member(
            open_id=open_id,
            session_key=session_key,
            level=1,
        )
        db.add(member_obj)
        db.flush()
    else:
        member_obj.session_key = session_key
        member_obj.last_login_at = datetime.now()
    
    db.commit()
    
    token = create_token(member_obj.id, member_obj.open_id)
    
    return success({
        "open_id": open_id,
        "session_key": session_key,
        "token": token,
        "member_id": member_obj.id,
    }, "登录成功")


@router.get("/info")
async def get_member_info(
    request,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """获取会员信息"""
    member_obj = db.query(Member).filter(Member.id == member_id).first()
    if not member_obj:
        return error(ERR_NOT_FOUND, "会员不存在")
    
    phone_display = None
    if member_obj.phone:
        phone_display = member_obj.phone[:3] + "****" + member_obj.phone[-4:]
    
    return success({
        "id": member_obj.id,
        "open_id": member_obj.open_id,
        "nickname": member_obj.nickname,
        "avatar_url": member_obj.avatar_url,
        "phone": phone_display,
        "level": member_obj.level,
        "created_at": member_obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    })


@router.put("/info")
async def update_member_info(
    body: UpdateMemberRequest,
    db: Session = Depends(get_db),
    member_id: int = Depends(get_current_member_id),
):
    """更新会员信息"""
    member_obj = db.query(Member).filter(Member.id == member_id).first()
    if not member_obj:
        return error(ERR_NOT_FOUND, "会员不存在")
    
    if body.nickname is not None:
        member_obj.nickname = body.nickname
    if body.avatar_url is not None:
        member_obj.avatar_url = body.avatar_url
    if body.phone is not None:
        # Check if phone already taken by another member
        existing = db.query(Member).filter(Member.phone == body.phone, Member.id != member_id).first()
        if existing:
            return error(ERR_BAD_REQUEST, "手机号已被其他会员绑定")
        member_obj.phone = body.phone
    
    db.commit()
    return success(message="更新成功")
