#!/bin/zsh
userName=$(whoami)
cd /Users/"$userName" || exit
mkdir BediGames
if [ $? = 1 ]
then
    echo There already exists folder \"BediGames\" in \"\Users\\$userName\". Delete it first!
    exit
fi
cd BediGames || exit
python3 -c "import pygame"
if [ $? = 1 ]
then
    python3 -m pip install pygame
    if [ $? = 1 ]
    then
        echo A fatal error occurred while trying to install \'pygame\' module. Probably python3 is missing.
        cd ..
        rmdir BediGames
    fi
fi
git clone https://github.com/SuperrMurlocc/Balls
if [ $? = 1 ]
then
    echo A fatal error occurred while trying to install game. Probably xcrun is missing. Try to run \"xcode-select --install\" command in Terminal.
    cd ..
    rmdir BediGames
fi
cd /Users/"$userName"/Desktop || exit
if test -f /Users/"$userName"/Desktop/Balls.sh
then
    echo "\"Balls.sh\" file already exists on your Desktop. Can I replace it?"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) rm Balls.sh; touch Balls.sh; break;;
            No ) exit;;
        esac
    done
else
    touch Balls.sh
fi
echo "#!/bin/zsh" >> Balls.sh
echo osascript -e \'tell application \"Terminal\" to set visible of front window to false\' >> Balls.sh
echo cd /Users/"$userName"/BediGames/Balls >> Balls.sh
echo git pull >> Balls.sh
echo python3 main.py >> Balls.sh
echo exit >> Balls.sh
chmod +x Balls.sh
touch HideExtension.scpt
echo tell application \"Finder\" >> HideExtension.scpt
echo set extension hidden of alias \"Macintosh HD:Users:$userName:Desktop:Balls.sh\" to true >> HideExtension.scpt
echo end tell >> HideExtension.scpt
osascript HideExtension.scpt
rm HideExtension.scpt
echo Installation complete!
exit
