# API-pagamento-credito
Mock de API de pagamento via cartão de crédito, livremente inspirado na API da Ebanx
Com ela, é possível simular em seus projetos pagamentos via cartão de crédito, inclusive validando diversos cenários de sucesso e erro!



Como utilizar essa API?

A API foi construída em Python, utilizando o Flask para exposição da função de pagamento de cartão de crédito via API REST. Para isso, execute o seguinte comando para iniciar a API:

```
$ python app.py
```

Por padrão, a API estará disponibilizada localmente na porta 5000 (http://localhost:5000/), sendo que ao executar no caminho padrão, deverá ser respondida a mensagem ˜Hello world˜, caso tudo esteja funcionando corretamente.

A API (mock) de pagamentos via cartão de crédito

1. URL para execução (POST): http://localhost:5000/api/v1/ws/direct

2. Contas disponíveis: o arquivo contém três contas, com números de cartão de crédito e bandeiras diferentes, cada um com limite inicial de R$ 2000,00. Conforme os cartões são utilizados, os limites são consumidos (basta fazer o restart da aplicação para reiniciar os limites:

```
{'card_number': {
    '4539479713709044': {
        'card_name': 'Jackson Johnson',
        'card_type': 'Visa',
        'card_due_date': '07/2041', 
        'card_cvv': '342',
        'available_limit': 2000,
        'document': '89311417009'},
     '5170904803237193': {
        'card_name': 'Abigail Robinson',
        'card_type': 'MasterCard',
        'card_due_date': '08/2049', 
        'card_cvv': '103',
        'available_limit': 2000,
        'document': '49605107066'},
      '342601535935862': {
        'card_name': 'Dominic Cox',
        'card_type': 'American Express',
        'card_due_date': '08/2049', 
        'card_cvv': '1218',
        'available_limit': 2000,
        'document': '49605107066'}
    }
}
```

3. Como executar a requisição: o seguinte JSON pode ser utilizado como base para executar um pagamento:

```
{
    "integration_key": "your_test_integration_key_here",
    "operation": "request",
    "payment": {
        "name": "José Silva",
        "email": "jose@example.com",
        "document": "89311417009",
        "address": "Rua E",
        "street_number": "1040",
        "city": "Maracanaú",
        "state": "CE",
        "zipcode": "61919-230",
        "country": "br",
        "phone_number": "(85)98680-7035",
        "payment_type_code": "creditcard",
        "merchant_payment_code": "3ad1f4096a2",
        "order_number": "12345-AA",
        "currency_code": "BRL",
        "instalments": 12,
        "amount_total": 90,
        "creditcard": {
            "card_number": "4539479713709044",
            "card_name": "Jackson Johnson",
            "card_due_date": "07/2041",
            "card_cvv": "342"
        }
    }
}
```

No geral, nenhum estado/atualização é realizado com os campos informados, apenas o valor é afetado, para controle do limite disponível.


4. Quais regras e validações são realizadas?

- Campos da requisição:

Campo | Tipo | Descrição | Obrigatório | Valores possíveis
----------------|-------|-----------------------|-----|-----------
integration_key | texto | Chave para integração | Sim | 
operation | texto | Define o tipo de operação (request) | Sim |
payment | objeto | Dados para execução do pagamento | Sim | 
payment - name | texto | Nome do pagador | Sim | 
payment - email | e-mail | E-mail do pagador | Sim | 
payment - document | texto | CPF do pagador | Sim | 
payment - address | texto | Endereço (rua, avenida etc.) | Sim | 
payment - street number | texto | Número referente ao endereço informado | Sim |
payment - state | texto | estado referente ao endereço informado | Sim |
payment - zipcode | texto | CEP referente ao endereço informado | Sim
payment - country | enum | país referente ao endereço informado | Sim | "br"
payment - phone_number | texto | telefone do cliente pagador | Sim
payment - payment_type_code | texto | Indica o tipo de pagamento. Neste caso, tipicamente se usa "creditcard" | Sim | 
payment - merchant_payment_code | texto | Código identificador do lojista resposável pela venda | Sim | 
payment - order_number | texto | Número do pedido relacionado ao pagamento | Sim | 
payment - currency_code | enum | Indica qual a moeda em que o pagamento será realizado | Sim | "EUR","BRL","MXN","PEN","USD","CLP","COP","ARS","BOB" 
payment - installments | númerico (inteiro) | Quantidade de parcelas em que o pagamento será realizado | Sim | 0 a 12
payment - amount_total | numérico (decimal) | Valor total do pagamento | Sim | Mínimo de 0.01
payment - credit_card | objeto | Detalhamento (dados) do cartão de crédito utilizado no pagamento | Sim
payment - credit_card - card_number | texto | Número do cartão de crédito utilizado no pagamento | Sim | 
payment - credit_card - card_name | texto | Nome do pagador, como indicado no cartão de crédito | Sim | 
payment - credit_card - card_due_date | texto | Data de vencimento indicado no cartão de crédito | Sim | 
payment - credit_card - card_cvv | texto | Card Verification Value: código de verificação do cartão | Sim | 

- Validação de dígito veriicador (Luhn checksum)

- Validação de códigos de bandeira/operadora existentes

- Validação de dados de cartão x contas (se todos os dados informados são os mesmos cadastrados)

- Validação de limites

Caso os dados não estejam corretos, será gerado uma resposta com código HTTP 400 (Bad Request)

Em caso de sucesso, será retornada uma resposta similar a essa:

```
{
    "payment": {
        "amount_br": 90,
        "amount_ext": 90,
        "amount_ext_requested": 90,
        "amount_iof": 0.38,
        "capture_available": false,
        "confirm_date": "2022-02-20 16:48:45",
        "country": "br",
        "currency_ext": "BRL",
        "currency_rate": 1.0,
        "details": {
            "billing_descriptor": "DEMONSTRATION"
        },
        "due_date": "2022-02-20",
        "hash": "5ef38bd200a530d9a4c218b054744cb81f9b25c99d4365aa",
        "instalments": 12,
        "merchant_payment_code": "3ad1f4096a2",
        "open_date": "2022-02-20 16:48:45",
        "order_number": "12345-AA",
        "payment_type_code": "creditcard",
        "pin": "025107300",
        "pre_approved": true,
        "status": "CO",
        "status_date": "2022-02-20 16:48:45",
        "transaction_status": {
            "acquirer": "EBANX",
            "code": "OK",
            "description": "Transaction captured"
        },
        "transfer_date": "Sun, 20 Feb 2022 16:48:45 GMT"
    },
    "status": "SUCCESS"
}
```

