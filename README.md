# todo-gnode

## Task description

    The task is to implement a small todo list web application. The
    application should display a list of todo items, each with a name
    description and date. Further it should be possible mark items in the
    todo list as "done" and to create and delete items.
    The todo list should be persisted on the server. A simple in memory
    store should be sufficient but you can of course also use a data base.

    You can use any language or framework to complete the task and you may
    keep the application as simple as possible. But it would be really great
    if one key aspect of the app would be somehow special (use an unusual
    language, design a beautiful UI, implement a REST API or a nice
    persistence layer, ...).


## Technical stuff

### Database

Database is in Mongodb. Documents have the following structure:

```
{
  user_id: string,
  description: string,
  date_due: date (optional),
  priority: int,
  done: boolean
}
```

### Web framework

Tordado (Python)
