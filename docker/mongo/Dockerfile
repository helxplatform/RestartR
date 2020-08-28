FROM mongo
ENV HOME /home
ENV USERNAME root
ENV PASSWORD  example

WORKDIR $HOME

ADD mongo_backup.sh .

CMD  /bin/bash $HOME/mongo_backup.sh $USERNAME $PASSWORD
