\# Contribuyendo a TalentHub RAG API



¡Gracias por tu interés en contribuir! Este documento proporciona directrices para contribuir al proyecto.



\## 🌟 Formas de Contribuir



\- 🐛 Reportar bugs

\- 💡 Sugerir nuevas características

\- 📝 Mejorar documentación

\- 🔧 Enviar pull requests



\## 🚀 Proceso de Contribución



\### 1. Fork y Clone

```bash

\# Fork el repositorio en GitHub

git clone https://github.com/tu-usuario/talenthub-rag-api.git

cd talenthub-rag-api

```



\### 2. Crear una Rama

```bash

\# Crear rama para tu feature

git checkout -b feature/mi-nueva-caracteristica



\# O para un bugfix

git checkout -b fix/descripcion-del-bug

```



\### 3. Configurar el Entorno

```bash

\# Crear entorno virtual

python -m venv venv

source venv/bin/activate  # Linux/Mac

\# o

venv\\Scripts\\activate  # Windows



\# Instalar dependencias

pip install -r requirements.txt

pip install pytest pytest-cov black flake8  # Dev dependencies

```



\### 4. Hacer Cambios



\- Escribe código limpio y bien documentado

\- Sigue las convenciones de estilo (PEP 8)

\- Agrega tests para nuevas funcionalidades

\- Actualiza la documentación si es necesario



\### 5. Ejecutar Tests

```bash

\# Ejecutar todos los tests

pytest



\# Con cobertura

pytest --cov=. --cov-report=html



\# Linting

black . --check

flake8 .

```



\### 6. Commit

```bash

\# Formato de commits

git commit -m "tipo: descripción breve



Descripción detallada si es necesario.



Closes #123"

```



\*\*Tipos de commit:\*\*

\- `feat`: Nueva característica

\- `fix`: Corrección de bug

\- `docs`: Cambios en documentación

\- `style`: Formato, punto y coma faltante, etc.

\- `refactor`: Refactorización de código

\- `test`: Agregar o modificar tests

\- `chore`: Mantenimiento general



\### 7. Push y Pull Request

```bash

git push origin feature/mi-nueva-caracteristica

```



Luego crea un Pull Request en GitHub con:

\- Título descriptivo

\- Descripción detallada de los cambios

\- Screenshots si es relevante

\- Referencias a issues relacionados



\## 📋 Checklist para Pull Requests



\- \[ ] El código sigue las convenciones de estilo del proyecto

\- \[ ] Se agregaron/actualizaron tests

\- \[ ] Todos los tests pasan

\- \[ ] Se actualizó la documentación

\- \[ ] El commit message es descriptivo

\- \[ ] No hay conflictos con la rama principal



\## 🎨 Guía de Estilo



\### Python



\- Seguir PEP 8

\- Usar type hints cuando sea posible

\- Documentar funciones con docstrings

\- Máximo 88 caracteres por línea (Black default)

```python

def buscar\_profesionales(

&nbsp;   query: str,

&nbsp;   filtros: Optional\[Dict] = None,

&nbsp;   top\_k: int = 5

) -> List\[Dict]:

&nbsp;   """

&nbsp;   Busca profesionales en la base vectorial.

&nbsp;   

&nbsp;   Args:

&nbsp;       query: Texto de búsqueda

&nbsp;       filtros: Filtros opcionales a aplicar

&nbsp;       top\_k: Número de resultados a retornar

&nbsp;       

&nbsp;   Returns:

&nbsp;       Lista de profesionales encontrados

&nbsp;   """

&nbsp;   pass

```



\### Commits

```

feat: agregar filtro por certificaciones



\- Implementa filtrado por certificaciones específicas

\- Agrega tests para el nuevo filtro

\- Actualiza documentación del endpoint



Closes #45

```



\## 🐛 Reportar Bugs



Usa el \[issue tracker](https://github.com/tu-usuario/talenthub-rag-api/issues) con:



1\. \*\*Título descriptivo\*\*

2\. \*\*Descripción del problema\*\*

3\. \*\*Pasos para reproducir\*\*

4\. \*\*Comportamiento esperado vs actual\*\*

5\. \*\*Entorno\*\* (OS, Python version, etc.)

6\. \*\*Screenshots\*\* si aplica



\### Template de Bug Report

```markdown

\*\*Descripción del Bug\*\*

Una descripción clara del problema.



\*\*Pasos para Reproducir\*\*

1\. Ir a '...'

2\. Ejecutar '...'

3\. Ver error



\*\*Comportamiento Esperado\*\*

Lo que debería suceder.



\*\*Screenshots\*\*

Si aplica, agregar capturas de pantalla.



\*\*Entorno:\*\*

\- OS: \[e.g. Ubuntu 22.04]

\- Python: \[e.g. 3.10.5]

\- Versión: \[e.g. 1.0.0]

```



\## 💡 Sugerir Características



Usa el issue tracker con el label `enhancement`:



1\. \*\*Descripción clara\*\* de la característica

2\. \*\*Motivación\*\*: ¿Por qué es útil?

3\. \*\*Ejemplos de uso\*\*

4\. \*\*Posibles implementaciones\*\*



\## 🧪 Tests



\### Escribir Tests

```python

def test\_busqueda\_con\_filtros():

&nbsp;   """Test búsqueda con múltiples filtros"""

&nbsp;   response = client.post(

&nbsp;       "/api/rag/search",

&nbsp;       json={

&nbsp;           "query": "Python developer",

&nbsp;           "filters": {

&nbsp;               "skills": \["Python"],

&nbsp;               "workMode": \["Remoto"]

&nbsp;           }

&nbsp;       }

&nbsp;   )

&nbsp;   assert response.status\_code == 200

&nbsp;   assert len(response.json()\["professionals"]) > 0

```



\### Ejecutar Tests Específicos

```bash

\# Test específico

pytest tests/test\_api.py::test\_busqueda\_con\_filtros -v



\# Por categoría

pytest -m "unit"  # tests marcados como @pytest.mark.unit

```



\## 📝 Documentación



\- Actualizar README.md si cambias funcionalidad

\- Documentar nuevos endpoints en docstrings

\- Agregar ejemplos de uso

\- Actualizar diagramas si es necesario



\## ❓ Preguntas



Si tienes preguntas:

\- Abre un issue con el label `question`

\- Contacta a los maintainers

\- Revisa issues existentes



\## 📜 Código de Conducta



\- Ser respetuoso y profesional

\- Aceptar críticas constructivas

\- Enfocarse en lo mejor para el proyecto

\- Mostrar empatía hacia otros contribuyentes



\## 🎉 Reconocimientos



Los contribuyentes son listados en:

\- README.md

\- Release notes

\- GitHub contributors page



---



¡Gracias por contribuir a TalentHub RAG API! 🚀

