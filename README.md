# Ionmix4 Editor

The python class here can be used to read in a .cn4 written in the ionmix4 format. You can then set the a temperature that will remove all entires from the tables corresponding to temperatures below that value. This can be useful when using databases such as SESAME EOS which contains -ve values for pressure and internal energy that cause numerical errors in the Flash simulation. This is described in more detial by P. Farmakis in [this poster](https://flash.rochester.edu/pipermail/flash-users/attachments/20221115/63e952bd/attachment-0001.pdf).

## Requirements

```zsh
numpy
```
