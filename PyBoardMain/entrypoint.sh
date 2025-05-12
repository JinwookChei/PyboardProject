#!/bin/sh

# DB 초기화 및 마이그레이션 (이미 되어 있으면 무시)
echo "Running database migrations..."

# 데이터베이스 초기화 (한 번만 실행)
if [ ! -d "migrations" ]; then
    flask db init
fi

# 데이터베이스 마이그레이션 생성
flask db migrate

# 데이터베이스 업그레이드
flask db upgrade

# Flask 앱 실행
exec "$@"