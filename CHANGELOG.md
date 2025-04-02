# Changelog

## [1.5.2] - 2025-04-01

### Fixed
- Fixed misleading docstring for `serializer.hs_serializer` and `serializer.get_hs_fields`

---

## [1.5.1] - 2025-04-01

### Changed
- `wrap` kwarg in `hs_dump` defaults to `True`

---

## [1.5.0] - 2025-04-01

### Breaking
- `show` kwarg renamed to `preserve`
- `translate` kwarg renamed to `camelize`
- Using `hs_expand` will raise an error unless removed or replaced with `hs_dump` using the `flatten` kwarg

### Changed
- Core functionality for building hyperscript has been turned into its own library [hyperscript-dump](https://github.com/LucLor06/hyperscript-dump)

### Deprecated
- `hs_expand` is now deprecated. Use the `flatten` kwarg in `hs_dump` instead.

---

## [1.4.1] - 2025-03-31

### Added
- Added [CHANGELOG.md](CHANGELOG.md)

---

## [1.4.0] - 2025-03-31

### Added
- Added basic model/queryset serialization

---

## [1.3.0] - 2025-03-28

### Added
- Added `class` kwarg for specifying output element classes

---

## [1.2.0] - 2025-03-27

### Added
- Added `event` kwarg for specifying assignment event

---

## [1.1.0] - 2025-03-27

### Added
- Added `debug` kwarg for logging assignemnts to console

---

## [1.0.3] - 2025-03-26

### Fixed
- Fixed f-string formatting in error handling in [hyperscript.py](django_hyperscript/templatetags/hyperscript.py)that caused parser errors

---

## [1.0.2] - 2024-11-17

### Fixed
- Fixed icon sizing in [README.md](README.md) and switched source to url instead of path

---

## [1.0.1] - 2024-11-17

### Added
- Added icon