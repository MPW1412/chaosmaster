# Access restrictions and rights management

## General concept of access restriction

The static parts of the (progressive) web-app, such as the vue.js frontend and everything in /public/ is publicly available.

Most parts of the API are restricted and only availble to logged in users.

## Accounts

Each account has the following structure:

 - real name
 - username
 - email
 - account type ( admin, user, guest_user), where guest user is a special feature that will be introduced later and will be used for distributed access accross multiple instances
 - API key in UUID format

## Groups

Can contain users or other groups. Groups in groups are possible!

## access to stored objects

### owningEntity

Unlike its name suggests, this field has nothing to do with rights management. It just tracks who the real owner of an object is, in a jurisdictional way.

It can be empty, a user or a group. It can be changed by everyone with right access to the object.

### read access

read access includes reading all fields of an object including the attached pictures.

And also the following things can be changed:

 - place of an object (containing object)
 - quantity
 - create a public share

Access can be given to a group or user.

### write access

full access to all fields

### public shares

Public sharing is a functionality, that any user with read access to a stored object, can make this object publicly availble via a long link.

A public share contains:

 - 64 character random string [a-zA-Z0-9] that is used as url: chaosmaster.io/public/shares/<string>
 - validation timeout (can be infinite or until a certain timestamp
 - uuid of the shared object

# required tables in database

 - users: as specified above
 - groups: uuid of the group, name of the group, admins and users can create groups
 - n-to-n relationships: group <--> group members which can be another group or a user, also if the member has only read or also right access to the group. Right access includes right access to all objects that are attached to this group and also changing the name of the group
 - public shares: as specified above





