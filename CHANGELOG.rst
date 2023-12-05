=========
Changelog
=========

Version 0.1
===========

- api_insee : a python helper to request sirene API on api.insee.fr

Version 2.0
===========
- Add API v3.11 support
- Add informations endpoint support
- Add capability to inject custom `AuthService` to `ApiInsee` constructor
- Drop unused exception `ParamsExeption`
- Replace class and methods violate PEP8 naming convention
    - Errors classes are renamed SubjectError
        - `AuthExeption` is renamed `AuthenticationError`
        - `RequestExeption` is renamed `RequestError`
    - Camel cased methods and properties are renamed to snake case
- Create more specific Exceptions
    - `InvalidCredentialsError` that extend `AuthenticationError` is raised when
      API return an invalid credential errors on token request
    - `UrlError` that extend `RequestError` is raised when API return a bad
      request error
- Drop `noauth` parameter in `ApiInsee` init method
