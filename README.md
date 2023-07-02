# Installation and Running

- Создайте файл `.env`
- Скопируйте содержимое из env_sample и поместите в `.env`
- Измените значения переменных в `.env`

## MacOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# create tables
python src/db/common.py

# run bot
python src/main.py
```

## Windows Powershell
```powershell
python3 -m venv .venv
source .\.venv\Scripts\activate
pip install -r requirements.txt

# create tables
python .\src\db\common.py

# run bot
python .\src\main.py
```

## Get Access Token
- вам понадобится создать приложение в вашем сообществе и найти ID этого приложения
- затем подставить ID приложения вместо `${APP_ID}` в ссылке ниже
`https://oauth.vk.com/authorize?client_id=${APP_ID}&scope=wall,offline&redirect_uri=https://oauth.vk.com/blank.html&response_type=token`
