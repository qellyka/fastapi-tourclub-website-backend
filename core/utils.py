import io
import json

from fastapi import Depends, HTTPException, Request, status, Form, Response
from jose import JWTError
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union

from core.config import settings
from core.security import decode_token
from crud.users import get_user_by_email_or_username
from db.session import get_async_session
import gpxpy

from schemas import (
    HikeBase,
    PassBase,
    HikeParticipantBase,
    ClubParticipantBase,
    ArticleBase,
    NewsBase,
    HikeUpdate,
)


async def get_current_user(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token"
        )
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )
        user = await get_user_by_email_or_username(session, username, None)
        if not user or not user.is_activated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
        )


def role_required(roles: List[str]):
    async def checker(user=Depends(get_current_user)):
        if not set(roles).intersection(set(user.roles or [])):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return user

    return checker


def gpx_to_geojson(file_obj: Union[str, io.IOBase]) -> dict:
    if isinstance(file_obj, str):
        with open(file_obj, "r", encoding="utf-8") as gpx_file:
            gpx = gpxpy.parse(gpx_file)
    else:
        if isinstance(file_obj, io.BytesIO):
            file_obj = io.TextIOWrapper(file_obj, encoding="utf-8")
        gpx = gpxpy.parse(file_obj)

    features = []

    # Tracks
    for track in gpx.tracks:
        segments_coords = []
        for seg in track.segments:
            coords = [
                [p.longitude, p.latitude]
                for p in seg.points
                if p.longitude is not None and p.latitude is not None
            ]
            if len(coords) >= 2:
                segments_coords.append(coords)

        if not segments_coords:
            continue

        geometry = (
            {"type": "LineString", "coordinates": segments_coords[0]}
            if len(segments_coords) == 1
            else {"type": "MultiLineString", "coordinates": segments_coords}
        )
        features.append(
            {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "kind": "track",
                    "name": track.name,
                    "number": track.number,
                },
            }
        )

    # Waypoints
    for w in gpx.waypoints:
        if w.longitude is None or w.latitude is None:
            continue
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [w.longitude, w.latitude],
                },
                "properties": {
                    "kind": "waypoint",
                    "name": w.name,
                    "desc": w.description,
                    "comment": getattr(w, "comment", None),
                    "symbol": w.symbol,
                    "elevation": w.elevation,
                    "time": w.time.isoformat() if getattr(w, "time", None) else None,
                },
            }
        )

    # Routes
    for r in gpx.routes:
        coords = [
            [p.longitude, p.latitude]
            for p in r.points
            if p.longitude is not None and p.latitude is not None
        ]
        if len(coords) >= 2:
            features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": coords},
                    "properties": {
                        "kind": "route",
                        "name": r.name,
                        "desc": r.description,
                    },
                }
            )

    return {"type": "FeatureCollection", "features": features}


def parse_hike_form(hike: str = Form(...)) -> HikeBase:
    return HikeBase.model_validate(json.loads(hike))


def parse_pass_form(pass_stmt: str = Form(...)) -> PassBase:
    return PassBase.model_validate(json.loads(pass_stmt))


def parse_participant_form(participant: str = Form(...)) -> ClubParticipantBase:
    return ClubParticipantBase.model_validate(json.loads(participant))


def parse_article_form(article: str = Form(...)) -> ArticleBase:
    return ArticleBase.model_validate(json.loads(article))


def parse_news_form(news: str = Form(...)) -> NewsBase:
    return NewsBase.model_validate(json.loads(news))


def parse_update_hike_form(update_data: str = Form(...)) -> HikeUpdate:
    return HikeUpdate.model_validate(json.loads(update_data))


def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRES_MINUTES * 60,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
    )


def generate_slug(title: str):
    return slugify(title)
