# Deezer to Spotify migration

## FRENCH (english version below)

### Lancez l'application
- Téléchargez la dernière release depuis GitHub, extrayez le zip obtenu quelque-part sur votre machine
- Lancez l'appli en faisant Clic Droit > Executer avec Powershell sur le fichier `setup.ps1`
- Après quelques minutes, un onglet devrait s'ouvrir dans votre navigateur avec une interface web:
    - ![Alt text](./readme_files/web_interface.png?raw=true "Web interface")

### Créez une application Spotify API
- Ouvrir https://developer.spotify.com/dashboard dans votre navigateur
- Authentifiez-vous avec votre compte Spotify
- Créez une nouvelle application:
    - Fournissez un nom et une description à votre application (exemple: "Deezer_Spotify" "Mon app de migration de chansons de Deezer vers Spotify")
    - Réglez la "Redirect URI" à la valeur suivante: http://localhost:8888
    - Cochez l'utilisation de la "Web API"
    - Ouvrez les paramètres de l'application
    - Copiez le Client ID et le Client Secret dans un bloc-notes (ou n'importe où)
        - ![Alt text](./readme_files/spotify_app.png?raw=true "Spotify API Application")

### Utilisez l'appli!
- Fournissez l'ID de la playlist Deezer à migrer (par exemple, l'ID de"https://www.deezer.com/fr/playlist/12836238621" est 12836238621)
- Fournissez les paramètres de votre application utilsant l'API de Spotify (Client ID, Client secret, redirect URI)
- Sélectionnez les chansons à migrer depuis la playlist Deezer
- Lancez la recherche de ces chansons dans Spotify et validez les résultats obtenus
- Générez la playlist (exemple ci-dessous)
    - ![Alt text](./readme_files/exemple.png?raw=true "Exemple")

## ENGLISH

### Run the app
- Download the latest release from GitHub and extract the archive somewhere on your computer
- Run the app right-click `setup.ps1` and execute it with Powershell
- After a few minutes, a tab should open in your browser displaying a web interface

### Create a Spotify API Application
- Go to https://developer.spotify.com/dashboard
- Authenticate using your Spotify account
- Create an app:
    - Provide an app name & description
    - Set the redirect URI to http://localhost:8888
    - Tick the usage of the Web API
    - Go to the app's settings
    - Copy the Client ID and the Client Secret into a notepad (or anywhere else)

### Use the app!
- Provide the ID of the Deezer playlist to migrate (for example, the id of "https://www.deezer.com/fr/playlist/12836238621" is 12836238621)
- Provide your Spotify API application parameters (Client ID, Client secret, redirect URI)
- Select the song to migrate from the Deezer playlist
- Search for these songs in Spotify & validate the findings
- Create the playlist