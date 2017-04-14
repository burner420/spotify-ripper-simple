# About
Spotify Ripper Simple is a frontend GUI for [spotify-ripper](https://github.com/SolidHal/spotify-ripper), which allows you to convert Spotify URIs/URLs to MP3s.  The goal of this frontend is to make it easy to setup and easy to use the amazing [spotify-ripper](https://github.com/SolidHal/spotify-ripper) software.

![Create](https://raw.githubusercontent.com/burner420/spotify-ripper-simple/master/screenshots/create.png)
![Progress](https://raw.githubusercontent.com/burner420/spotify-ripper-simple/master/screenshots/progress.png)


# Requirements
i) You must have a Spotify Premium Account.
ii) You need a Spotify App Key.  Spotify stopped issuing these but maybe you can find one :) .
iii) A computer with an internet connection -- Spotify Ripper Simple runs on Docker and is compatible with Linux, OSx, Windows, and any operating system that supports Docker.

# Installation
## 1. Install Docker
Install Docker Community Edition.  Installation instructions can be found on the [Docker Website](https://docs.docker.com/engine/installation/).

## 2. Download Spotify Ripper Simple
i) Download this repository - click "Clone or Download" > "Download Zip"
ii) Extract the downloaded zip file to a folder on your computer

## 3. Build Image
This step may take some time (5-10 minutes) to install, configure and build the software.

### Linux/OSX
i) Open Terminal
ii) Navigate to the extracted folder from the previous step - `cd /my/folder/spotify-ripper-simple`
iii) Build Image - `docker build -t spotify-ripper-simple .`

### Windows
i) Open Command Prompt - Start -> Run -> cmd.exe
ii) Navigate to the extracted folder from the previous step - `cd /my/folder/spotify-ripper-simple`
iii) Build Image - `docker build -t spotify-ripper-simple .`

## 4. Start Software
i) Start Software - from the terminal (or windoze command prompt) issue the command: `docker run -d -p 5000:5000 spotify-ripper-simple`
ii) Navigate your web browser to http://localhost:5000

# Usage
## Initial Setup
![Setup](https://raw.githubusercontent.com/burner420/spotify-ripper-simple/master/screenshots/setup.png)
During the initial setup you will be required to provide a Spotify App Key and your Spotify credentials.  Double-check these are correct before going to the next step since the App Key and credentials aren't verified until you actually start ripping.
If you created your Spotify account using Facebook, you can use your Facebook email address and request your password from Facebook - See the [Facebook Help Page](https://www.facebook.com/help/249378535085386?helpref=uf_permalink) for more info.

## Creating a Rip
i) Go to the Rips page
ii) Click "Create New Rip"
![Create](https://raw.githubusercontent.com/burner420/spotify-ripper-simple/master/screenshots/create.png)
iii) Open Spotify and select the songs you want to rip
iv) Copy the songs (keyboard shortcut or File menu)
v) Paste these songs into your web browser
![Configure Rip](https://raw.githubusercontent.com/burner420/spotify-ripper-simple/master/screenshots/configure_rip.png)
vi) Name your rip (optional but helpful to track your rips)
vii) Click "Go!"
iix) That's it!  Once your rip is complete you will be able to download the songs as a zip file
![Progress](https://raw.githubusercontent.com/burner420/spotify-ripper-simple/master/screenshots/progress.png)

## Settings
On the settings page you can change the naming and create a custom folder hierarchy.  See the [documentation](https://github.com/SolidHal/spotify-ripper#user-content-format-string) in the upstream repo for formatting details.

![Settings](https://raw.githubusercontent.com/burner420/spotify-ripper-simple/master/screenshots/settings.png)