## Plan: Tickets, anonimización y roles

Queremos transformar la app en un sistema de incidencias con dos perfiles claros, ticketing real, anonimización previa al almacenamiento, PostgreSQL como persistencia y dos modelos Random Forest expuestos como servicio aparte. La recomendación es mantener el backend FastAPI como orquestador, mover la inferencia de ML a un servicio/container independiente, y usar una tabla principal de tickets anonimizados con campos de control para predicción, revisión manual y trazabilidad.

**Steps**
1. Definir el contrato funcional y de datos del ticket, incluyendo el flujo ciudadano -> anonimización -> inferencia -> persistencia -> revisión admin. Este paso bloquea el diseño técnico del resto.
2. Crear el esquema de datos principal para tickets anonimizados, con campos de entrada originales separados del resultado persistido, y añadir columnas de control para urgencia del modelo, urgencia final del admin, categoría predicha, categoría final, estado y timestamps. *Depende de 1*.
3. Añadir PostgreSQL al entorno de desarrollo con un nuevo contenedor en `docker-compose.yaml`, variables de conexión en backend y frontend si hace falta, y un mecanismo de arranque/migración inicial para la tabla de tickets. *Depende de 2*.
4. Crear una capa de servicios en backend para tickets: validación de entrada, anonimización de `tlfno`, `nif`, `nombre`, `apellidos` y `email`, llamada al servicio de ML, y persistencia de la versión anonimizada. Este paso debe ejecutarse antes de cualquier insert en BD. *Depende de 2 y 3*.
5. Diseñar el servicio aparte de inferencia de ML, con dos endpoints o dos modelos cargados: uno para clasificar urgencia y otro para clasificar categoría. El backend llamará a este servicio en el momento de crear el ticket, y el admin podrá sobrescribir resultados más tarde. *Depende de 1 y 3*.
6. Reforzar la autenticación y autorización por rol en backend y frontend para separar rutas de ciudadano y admin, reutilizando lo ya existente pero ampliándolo a rutas de tickets y dashboard. *Puede avanzar en paralelo con 3, 4 y 5 una vez cerrado el contrato de datos*.
7. Construir el flujo ciudadano en frontend: formulario de alta de incidencia, confirmación de envío y vista de tickets propios. Debe consumir el backend y no exponer datos personales ya anonimizados. *Depende de 4*.
8. Construir el dashboard de admin: tickets pendientes de revisar, tickets no resueltos, selector para aceptar o modificar urgencia y categoría, y métricas básicas. Debe leer estado y permitir guardar la decisión final. *Depende de 4 y 6*.
9. Añadir estadísticas agregadas mínimas en backend para el dashboard admin, como total de tickets, abiertos, pendientes de revisión, resueltos, distribución por urgencia y por categoría. *Depende de 2 y 4*.
10. Validar el flujo end-to-end con pruebas de API, pruebas del anonimizado, pruebas de acceso por rol y una verificación manual del recorrido ciudadano/admin. *Depende de 4, 5, 7 y 8*.

**Team Assignment**
- Persona 1: contrato funcional y modelo de datos. Debe cerrar el flujo ciudadano -> anonimización -> inferencia -> persistencia -> revisión admin, definir el esquema de ticket y las reglas de estado. Es la base para todos los demás, así que bloquea 2, 3, 4, 5, 7, 8 y 9.
- Persona 2: infraestructura y BD. Debe añadir PostgreSQL al `docker-compose.yaml`, variables de entorno, conexión desde backend y migración/arranque inicial de la tabla principal. Depende de que Persona 1 cierre el esquema de datos y desbloquea 4, 5 y 9.
- Persona 3: servicio de ML. Debe crear el servicio aparte con los dos Random Forest, definir sus contratos de inferencia y dejar listo el consumo desde backend. Depende de Persona 1 y de que Persona 2 tenga el entorno/servicio de BD y despliegue definidos; desbloquea 4, 8 y 10.
- Persona 4: backend de negocio. Debe implementar la anonimización previa al guardado, crear y consumir el servicio de tickets, persistir la versión anonimizada y exponer endpoints para ciudadano y admin. Depende de Personas 1, 2 y 3; desbloquea 7, 8, 9 y 10.
- Persona 5: frontend y experiencia de usuario. Debe construir el flujo ciudadano de alta y listado de tickets, el dashboard de admin, el consumo del API y la navegación por rol. Puede avanzar en paralelo con parte del trabajo de Persona 4 una vez el contrato de endpoints esté definido; depende funcionalmente de 1 y 4, y para el dashboard completo también de 9.

**Suggested parallelization**
1. En paralelo: Persona 1 define contrato y Persona 2 prepara PostgreSQL/infra.
2. Después: Persona 3 prepara el servicio ML mientras Persona 4 diseña la capa de tickets del backend.
3. En cuanto exista el primer contrato estable de endpoints: Persona 5 arranca frontend con mocks o datos de prueba.
4. Cierre final: Personas 3, 4 y 5 integran, y Persona 1 valida que el flujo final respete el contrato y el histórico de cambios.

**Relevant files**
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/backend/src/app.py` - registrar nuevos routers y mantener la composición de la API.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/backend/src/deps.py` - centralizar autenticación/autorización por rol.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/backend/src/models/auth.py` - extender el usuario actual si se necesita más contexto de rol.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/backend/src/services/auth_service.py` - punto actual de mock auth; sirve como referencia para el nuevo contrato de login.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/backend/src/routers/admin_router.py` - ruta base para el dashboard de admin y futuras operaciones de revisión.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/backend/src/routers/citizen_router.py` - ruta base para el dashboard y creación de incidencias del ciudadano.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/backend/src/constants.py` - ubicación actual de datos mock; conviene reemplazarlo por persistencia real.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/docker-compose.yaml` - añadir el contenedor de PostgreSQL y, si se decide, el servicio de inferencia.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/frontend/routes/pages.py` - redirecciones por rol y futuras páginas de tickets.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/frontend/routes/auth.py` - login y sesión por rol.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/frontend/services/api_client.py` - cliente HTTP para endpoints de tickets y dashboards.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/frontend/templates/admin_dashboard.html` - UI de revisión y estadísticas.
- `c:/Users/A200525997/OneDrive - Deutsche Telekom AG/Desktop/CiudadIA/frontend/templates/citizen_dashboard.html` - UI del ciudadano para creación y seguimiento.

**Verification**
1. Probar login de admin y ciudadano y comprobar que cada uno solo entra a su dashboard correspondiente.
2. Enviar un ticket de prueba y verificar que los campos personales quedan anonimizados en la BD antes del insert.
3. Verificar que el servicio de inferencia devuelve urgencia y categoría y que el backend los guarda como predicción inicial.
4. Revisar que el admin puede cambiar urgencia y categoría y que el ticket queda marcado con valores finales.
5. Comprobar en el dashboard admin que aparecen tickets pendientes, no resueltos y estadísticas agregadas.
6. Ejecutar tests del backend y una prueba manual end-to-end con Docker Compose.

**Decisions**
- El servicio de ML debe ir aparte del backend FastAPI para desacoplar inferencia y facilitar mantenimiento.
- Se guarda histórico de cambios para poder comparar la salida del modelo con la decisión final del admin.
- Se usará una tabla principal de tickets anonimizados con campos de control, en lugar de repartir la información base en varias tablas.
- La anonimización ocurre antes de persistir en BD; los datos personales crudos no deben almacenarse.

**Further Considerations**
1. Conviene definir si la anonimización será irreversible o si habrá un esquema de pseudonimización con claves internas para soporte/auditoría.
2. Falta cerrar si el servicio de ML usará un único endpoint con dos predicciones o dos endpoints separados para urgencia y categoría.
3. Falta decidir si el dashboard admin se alimentará con polling, refresh manual o un canal más reactivo como WebSockets en una segunda fase.
