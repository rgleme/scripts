# CHARGE API

This project implements an API that register credit cards and authorizes a transaction for a specific account, following some predefined rules.

## Instructions

This project cand read any *.json using it as argument

## Requirements

docker, sqlite3

## Instructions


## Create Database

```bash
sqlite3 charge.db
```

```sql
CREATE TABLE charge (
    card_id INTEGER PRIMARY KEY,
    card_number NUMBER NOT NULL UNIQUE,
    card_limit NUMBER NOT NULL,
    card_status BOOL NOT NULL,
    last_transaction TEXT NOT NULL    
);
```

## Installation

Build the image with the Dockerfile

```bash
docker build -t charge__api .
```

## Usage

```docker
docker run -it --rm --name python_flask -v "$PWD":/usr/src/app/:rw -p 80:7000 -w /usr/src/app charge_api python main.py
```

## Add a Credit Card

```bash
curl -XPOST -d "@credit_cards/card1.json" -H "Content-Type: application/json" http://127.0.0.1/addcard
```

## Send a transaction

```bash
curl -XPOST -d "@transactions/transaction1.json" -H "Content-Type: application/json" http://127.0.0.1/transaction
```

## Run Tests

There are three tests: Json Schema, Credit Card lenght number and Invalid transaction Number

```bash
docker run -it --rm --name python_flask_test -v "$PWD":/usr/src/app/:rw -w /usr/src/app/tests charge_api python run.py test_json.py /usr/src/app/transactions/transaction1.json
```
