# github 연결
```
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/koeunyeon/devmini.git
git push -u origin main
```

# create virtualenv
```
python -m virtualenv venv
```

# install fastapi
```
. venv/Scripts/activate
pip install fastapi
pip install uvicorn
```

# vscode python 경로 지정
ctrl + shift + p
python: select interpreter

# vscode project root 경로 지정
`.env`
```
PYTHONPATH=server
```

# basic architacture 구성
## DB 관련 패키지
```
pip install pyyaml
pip install sqlalchemy[asyncio]
pip install aiomysql
```

# 이메일 validator 추가.
```
pip install pydantic[email]
```

# 회원 테이블 생성
```
table member: email.nn, email_key, expired_at, status.default=email_not_confirmed.nn
```
```
CREATE TABLE `member`
(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;

ALTER TABLE `member` ADD `email` VARCHAR(255) NOT NULL  ;
ALTER TABLE `member` ADD `email_key` VARCHAR(255) NULL  ;
ALTER TABLE `member` ADD `expired_at` datetime NULL  ;
ALTER TABLE `member` ADD `status` VARCHAR(255) NOT NULL DEFAULT 'email_not_confirmed' ;
ALTER TABLE `member` ADD `created_at` datetime NOT NULL  DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE `member` ADD `updated_at` datetime NULL  on update CURRENT_TIMESTAMP;
ALTER TABLE `member` ADD `use_yn` CHAR(1) NOT NULL DEFAULT 'Y' ;
```

# 회원 가입 로직 추가.
memberservice.py