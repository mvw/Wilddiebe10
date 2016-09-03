#!/bin/sh

# empty defaults
BACKUP_DIRS=
BACKUP_FILENAME=
GPG_PASS=
REMOTE_HOST=
REMOTE_USER=
SSH_KEYFILE=

if [[ -z $BACKUP_DIRS ]] || [[ -z $BACKUP_FILENAME ]] || [[ -z $GPG_PASS ]] || [[ -z $REMOTE_HOST ]] || [[ -z $SSH_KEYFILE ]]
then
  echo "Cannot create backup, because a mandatory configuration is missing."
  exit 1
fi

# Create tar.gz archive
tar cvzf ${BACKUP_FILENAME} ${BACKUP_DIRS}

# Encrypt archive 
gpg --yes --batch --passphrase="${GPG_PASS}" -c ${BACKUP_FILENAME}

# Remove unencrypted file
rm ${BACKUP_FILENAME}

# Copy backup to second fileserver
scp -i ${SSH_KEYFILE} ${BACKUP_FILENAME}.gpg ${REMOTE_USER}@${REMOTE_HOST}:${BACKUP_FILENAME}.gpg
