# Publier une version sur PyPI

Une version publiée sur PyPI ne peut ni être modifiée ni être republiée sous le même numéro : testez d'abord sur TestPyPI.
La publication utilise **Trusted Publishing** (GitHub prouve son identité à PyPI) : aucun jeton n'est stocké.

## Une seule fois

1. Créer un compte sur <https://pypi.org> (et sur <https://test.pypi.org>), avec l'authentification à deux facteurs.
2. Sur PyPI → *Your account* → *Publishing* → **Add a new pending publisher** :
   - nom du projet : `aiworkpay`
   - propriétaire : `AiWorkPay-SASU`, dépôt : `AIWorkPay-SDK-v1`
   - workflow : `publish.yml`, environnement : `pypi`

   Même chose sur TestPyPI avec l'environnement `testpypi`.
3. Sur GitHub → *Settings* → *Environments* : créer `pypi` et `testpypi`. Sur `pypi`, ajouter un *required reviewer*
   pour valider chaque publication à la main.
4. Fusionner la branche `claude/sdk-v2` dans la branche principale.

## À chaque version

1. Changer le numéro dans `aiworkpay/_version.py` **et** `pyproject.toml` (le workflow refuse s'ils diffèrent).
2. *Actions* → *Publish* → *Run workflow* → `testpypi`, puis tester :
   `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ aiworkpay`
3. Lancer à la main *Actions → Publish → Run workflow* : `target = testpypi` d'abord (essai à blanc), puis `target = pypi` avec
   `confirm` = `PUBLISH v<version> TO PYPI` (par exemple `PUBLISH v2.0.0 TO PYPI`). Le workflow construit, vérifie (`twine check`,
   installation du wheel dans un environnement vierge) puis publie. **Créer une Release GitHub ne publie plus rien** (le déclencheur
   `release` a été retiré pour qu'un clic ne puisse pas publier par accident). Trois verrous : la phrase de confirmation, l'environnement
   GitHub `pypi` avec *Required reviewers* (Settings → Environments), et le *publisher* de confiance déclaré sur PyPI.

Après la première publication, le « pending publisher » devient un publisher normal du projet `aiworkpay`.
