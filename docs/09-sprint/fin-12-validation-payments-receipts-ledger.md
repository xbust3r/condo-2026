# FIN-12 — Validación: Payments, Receipts, Ledger

**Fecha:** 2026-05-01
**Autor:** Bulma S (Review)
**Estado:** ✅ Validado — sin cambios requeridos

---

## Resumen

Los módulos `payments`, `receipts` y `ledger` fueron auditados contra el nuevo flujo
de prorrateo (FIN-02 a FIN-11). La conclusión es que **no requieren cambios**.

---

## Metodología

Code review exhaustiva de los 3 módulos, verificando puntos de acoplamiento con `charges` y `accounts_receivable`.

---

## 1. Payments

**Archivos revisados:**
- `core_payments/domain/payment_entity.py`
- `core_payments/infrastructure/dbpayment.py`
- `core_payments/infrastructure/payment_cmd_repository.py`
- `core_payments/usecase/payment_usecase.py`

**Puntos de integración con AR:**
- `payment_usecase.create()` → referencia a AR por `ar_id`
- VALIDACIÓN PAY-01: `amount ≤ ar.pending_amount` — comparación aritmética sobre Decimals
- El pago se registra con `ar_id` y `receipt_id`, sin leer `charge`
- `add_payment()` en AR recalcula `paid_amount += payment.amount` y actualiza status

**Veredicto:** ✅ Compatible. El pago solo necesita `ar_id` + `amount`. No lee `charge.amount` ni `charge.scope`.

### Flujo validado

| Escenario | Resultado esperado |
|---|---|
| Pago parcial en AR prorrateado | `status → partial`, `pending_amount` correcto |
| Pago total en AR prorrateado | `status → paid`, `pending_amount = 0` |
| Pago excede pending | `PaymentExceedsBalance` ✅ |
| Multiple pagos parciales | `paid_amount` acumula correctamente |

---

## 2. Receipts

**Archivos revisados:**
- `core_receipts/domain/receipt_entity.py`
- `core_receipts/infrastructure/dbreceipt.py`
- `core_receipts/infrastructure/receipt_cmd_repository.py`
- `core_receipts/usecase/receipt_usecase.py`

**Puntos de integración:**
- `receipt_number` auto-incremental por `condominium_id`
- Referencia a AR por `ar_id`
- Referencia a `unit_id`, `payer_user_id`
- Sin dependencia en `charge` o lógica de prorrateo

**Veredicto:** ✅ Compatible. Recibos son correlativos por condominio — independientes del monto.

### Verificación

| Check | Resultado |
|---|---|
| Recibo correlativo por condominio | ✅ `get_next_receipt_number()` |
| Recibo referencia AR correctamente | ✅ FK `ar_id` |
| Recibo con monto prorrateado | ✅ `amount_paid` es Decimal |

---

## 3. Ledger

**Archivos revisados:**
- `core_ledger_entries/domain/ledger_entity.py`
- `core_ledger_entries/infrastructure/db_ledger.py`
- `core_ledger_entries/infrastructure/ledger_cmd_repository.py`
- `core_ledger_entries/infrastructure/ledger_query_repository.py`
- `core_ledger_entries/usecase/ledger_usecase.py`

**Puntos de integración:**
- Referencia a `ar_id`, `payment_id`, `charge_id` (FKs opcionales)
- `debit` / `credit` / `balance` — operaciones aritméticas sobre Decimal
- `balance` running total por unidad
- Sin dependencia en el cálculo de prorrateo

**Veredicto:** ✅ Compatible. Ledger entries registran débitos/créditos con referencias FK,
  no calculan montos. El balance es aritmético.

### Verificación

| Check | Resultado |
|---|---|
| Débito AR prorrateado | ✅ `debit` = `entry.amount` |
| Crédito por pago | ✅ `credit` = `payment.amount` |
| Balance running | ✅ `balance` acumula correctamente |
| FKs a charge/payment/AR | ✅ Todas nullable, sin cascada |

---

## 4. Balance Summary

**Archivos revisados:**
- `ar_query_repository.get_summary_by_unit()`
- `ar_query_repository.get_summary_by_condominium()`

**Lógica:** Agrega `amount - paid_amount` por unidad/condominio. Puramente aritmético.

**Veredicto:** ✅ Compatible. Suma de Decimals prorrateados = total correcto.

---

## Conclusión

**No se requieren cambios en payments, receipts, ni ledger.**

La decisión arquitectónica original fue correcta: el prorrateo vive entre `charge` y `AR`.
Una vez que AR tiene el monto correcto (prorrateado), todo el pipeline downstream funciona
sin modificaciones porque opera sobre `ar.amount` y `ar.paid_amount` como valores opacos.

### Módulos tocados en este sprint

| Módulo | Cambios |
|---|---|
| `core_charges` | ✅ FIN-02+03 (scope, modelo) |
| `core_charges/domain` | ✅ FIN-04 (ProrationService) |
| `core_charges/usecase` | ✅ FIN-05+06 (ProrationUsecase) |
| `core_accounts_receivable` | ✅ FIN-08+09+10+11 (generate_from_charge, deudor, idempotencia, recurrencia) |
| `core_payments` | ❌ Sin cambios |
| `core_receipts` | ❌ Sin cambios |
| `core_ledger_entries` | ❌ Sin cambios |
