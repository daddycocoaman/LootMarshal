# `lootmarshal`

**Usage**:

```console
$ lootmarshal [OPTIONS] COMMAND [ARGS]...
```

**Commands**:

* `connect`: Connects to a specified handler
* `secret`: Interact with secrets
* `server`: Starts the LootMarshal server

## `lootmarshal connect`

Connects to a specified handler

**Usage**:

```console
$ lootmarshal connect [OPTIONS] COMMAND [ARGS]...
```

**Commands**:

* `azure`: Connects to Azure.

### `lootmarshal connect azure`

Connects to Azure.

**Usage**:

```console
$ lootmarshal connect azure [OPTIONS]
```

## `lootmarshal secret`

Interact with secrets

**Usage**:

```console
$ lootmarshal secret [OPTIONS] COMMAND [ARGS]...
```

**Commands**:

* `get`: Gets a secret.
* `set`: Sets a secret.

### `lootmarshal secret get`

Gets a secret.

**Usage**:

```console
$ lootmarshal secret get [OPTIONS] NAME
```

### `lootmarshal secret set`

Sets a secret.

**Usage**:

```console
$ lootmarshal secret set [OPTIONS] NAME VALUE CONTENT_TYPE
```

## `lootmarshal server`

Starts the LootMarshal server

**Usage**:

```console
$ lootmarshal server [OPTIONS]
```
