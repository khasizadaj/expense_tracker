# Architecture - Expense Tracker

### Database

- `categories` table

  - `id` : `int`
  - `name` : `str`

- `expenses` table

  - `id` : `int`
  - `date` : `date`
  - `amount` : `decimal`
  - `category_id` : `int` (connects to `categories` table)
  - `note` : `str` (optional)
  - `active` : `bool`

> `active` field in `expenses` table stores boolean value and represents if expenses is deleted
> or not.
