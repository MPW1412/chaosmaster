<template>
  <v-app>
    <div>
      <v-app-bar>    
        <v-spacer></v-spacer>  
        <v-btn small class="ma-2"
          id="#createBtn"
          v-on:click="createStoreObject">
          Create
        </v-btn>
        <v-btn small class="ma-2"
          id="#browseBtn"
          v-on:click="BrowseMode">
          Browse
        </v-btn>
      </v-app-bar>
    </div>

    <v-container class="space-for-bottom">
      <v-row no-gutters v-if="storeObject.length > 0">
        <v-col
          v-for="n in storeObject"
          :key="n.uuid"
          cols="12"
          class="p-10"
          sm="4">
          <v-layout>
            <v-flex>
              <v-card
                class="pa-2 m-b-0">
                <v-row>
                  <v-col sm="8" cols="8">
                    <v-card-title v-if="n.name">
                      {{n.name}}            
                    </v-card-title>
                    <v-card-text v-else>
                      {{n.uuid}}
                    </v-card-text>
                  </v-col>
                  <v-col sm="4" cols="4">
                    <v-btn text color="warning" dark
                      v-on:click="getStoredObjectImages(n.uuid)"
                      id="#storedObjectImages">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>                
                <v-card-text v-if="n.description">
                  {{n.description.substring(0,100)}}
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-col>
      </v-row>
    </v-container>

    <v-bottom-navigation
      fixed
      position="absolute"
      background-color="#03fcf0">
      <v-spacer></v-spacer>
      <v-bottom-sheet
        v-model="sheet" >
        <template v-slot:activator="{ on }">
          <v-btn
            id="cameraBtn"
            fab
            color="#03fcf0"
            v-on="on">
            <v-icon>mdi-camera</v-icon>
          </v-btn>
        </template>

        
        <v-sheet height="300px">
          <v-row>
            <v-col cols="4">
              <div id="scaleVideo">
                <!-- <video ref="video" id="video" width="1280" height="720" autoplay></video> -->
                <qrcode-stream @decode="onDecode" @init="onInit" />
                <vue-webcam ref='webcam' />
              </div>
            </v-col>
            <v-col cols="8">
              <p v-if="error">{{ error }}</p>
              <p>UUID: <b>{{ currentUUID }}</b></p>
              <v-btn @click="takePhoto"
                :disabled="photos.length >= 10">
                Take Photos
              </v-btn>
              <v-row style="overflow-y: auto; height: 250px; padding: 15px;"
                no-gutters v-if="photos.length > 0 || selectedPhotos.length > 0">
                <v-col
                  v-for="n in photos"
                  :key="n"
                  cols="12"
                  sm="2">
                    <img :src="n" alt="" v-if="itemsContains(n)"
                      style="width:100px;height:100px" 
                      class= "preview-selected-image"
                      @click="selectedPhotos(n)"/>
                    <img :src="n" alt="" v-else
                      style="width:100px;height:100px" 
                      class= "preview-image"
                      @click="selectedPhotos(n)"/> 
                    <v-btn class="custom-button-delete"
                      @click="removePhoto(n)">
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-sheet>
      </v-bottom-sheet>
    </v-bottom-navigation>

    <v-layout row justify-center>
      <v-dialog v-model="addObject" fullscreen transition="dialog-bottom-transition">
        <v-card class="v-card-images">
          <v-toolbar color="#03fcf0">
            <v-btn icon @click="closeCreateForm">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>Add New Object</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn small class="ma-2"
              id="#saveBtn"
              v-on:click="saveStoreObject">
              Save
            </v-btn>
          </v-toolbar>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12 sm5 v-if="currentUUID === ''">
                  <v-text-field label="UUID" hide-details="auto"
                    @change="changeInputValue($event,'uuid', false)"
                    :rules="uuidRules"
                    ref="uuid">
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm5 v-else>
                  <v-text-field label="UUID" hide-details="auto"
                    :value="currentUUID"
                    @change="changeInputValue($event,'uuid', false)"
                    :rules="uuidRules"
                    ref="uuid"
                    readonly>
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm2>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-select
                  item-text="value"
                  item-value="id"
                  :items="types"
                  label="Type"
                  @change="changeInputValue($event,'type', false)"
                  ref="type"></v-select>
                </v-flex>
                <v-flex xs12>
                  <v-text-field label="Name" hide-details="auto"
                    @change="changeInputValue($event,'name', false)"
                    :rules="nameRules"
                    ref="name">
                  </v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field label="Description" hide-details="auto"
                    @change="changeInputValue($event,'description', false)"
                    ref="description">
                  </v-text-field>
                </v-flex>      
                <v-flex xs12>
                  <v-text-field label="Purpose" hide-details="auto"
                    @change="changeInputValue($event,'purpose', false)"
                    ref="purpose">
                  </v-text-field>
                </v-flex>  
                <v-flex xs12 sm5>
                  <v-checkbox label="Nestable"
                    @change="changeInputValue($event,'nestable', true)"
                    ref="nestable">
                  </v-checkbox>
                </v-flex>
                <v-flex xs12 sm2>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-checkbox label="Completed"
                    @change="changeInputValue($event,'completed', true)"
                    ref="completed">
                  </v-checkbox>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Owning Entity" hide-details="auto"
                    @change="changeInputValue($event,'owningEntity', false)"
                    :rules="uuidRules"
                    ref="owningEntity">
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm2>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Location Entity UUID" hide-details="auto"
                    @change="changeInputValue($event,'locationEntityUUID', false)"
                    :rules="uuidRules"
                    ref="locationEntityUUID">
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Visibility" hide-details="auto"
                    @change="changeInputValue($event,'visibility', true)"
                    :rules="numberRules"
                    ref="visibility">
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm2>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Quantity" hide-details="auto"
                    @change="changeInputValue($event,'quantity', true)"
                    :rules="numberRules"
                    ref="quantity">
                  </v-text-field>
                </v-flex>
              
                <v-flex xs12 sm5>
                  <v-text-field label="Category" hide-details="auto"
                    @change="changeInputValue($event,'category', true)"
                    :rules="numberRules"
                    ref="category">
                  </v-text-field>
                </v-flex>
                  <v-flex xs12 sm2>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Standarised Object" hide-details="auto"
                    @change="changeInputValue($event,'standarisedObject', false)"
                    :rules="uuidRules"
                    ref="standarisedObject">
                  </v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-layout>
    <v-snackbar
      :timeout="3000"
      :top=true
      :right=true
      :multi-line=true
      :vertical=true
      v-model="snackbar">
      {{message}}
      <v-btn text color="pink" @click.native="snackbar = false">
        Close
      </v-btn>
    </v-snackbar>
    <v-layout row justify-center>
      <v-dialog v-model="createObject" persistent max-width="290">
        <v-card class="dialog-custom">
          <div class="p-25">
            <v-card-title class="headline">Are You Sure?</v-card-title>
            <v-card-text>Click Yes, if you want to create store object else Click No</v-card-text>
          </div>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" 
              @click="createObject = false">
              No
            </v-btn>
            <v-btn color="green" 
              v-on:click="createStoreObjectWithUUID">
              Yes
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </v-app>
</template>

<script>
import storeObjectApi from '../api/storedObject';
import imagesApi from '../api/images';
import nestableObjectApi from '../api/nestableObject';
import { QrcodeStream } from 'vue-qrcode-reader';
import VueWebcam from "vue-webcam";

export default {
  name: 'Home',

  components: { 
    QrcodeStream,
    VueWebcam
  },

  data(){
    return {
      currentUUID: '',
      previousUUID: '',
      error: '',
      sheet:'',
      storeObject:'',
      images:'',
      addObject:false,
      snackbar: false,
      createObject: false,
      message:'',
      create: false,
      photos:[],
      selectedPhotosList:[],
      types: [
        {
          id: 1, 
          value:'type1'
        },
        {
          id: 2, 
          value:'type2'
        }
      ],
      form:{
        // uuid:'',
        // name:'',
        // description:'',
        // purpose:'',
        // owningEntity:'',
        // locationEntity:'',
        // visibility:'',
        // quantity:'',
        // category:'',
        // standarisedObject:''
      },
      uuidRules: [
        v => {
          if (v) return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(v) || 'Not a Valid UUID'
          else return true;
        },
      ],
      nameRules: [
        v => {
          if (v) return v.length <= 20 || 'Not more than 20 characters';
          else return true;
        },
      ],
      numberRules: [
        v => {
          if (v) return !isNaN(v) || 'Must be Number';
          else return true;
        },
      ],
    }
  },

  methods: {

    takePhoto() {
      const getPhoto = this.$refs.webcam.getPhoto();
      this.photos.push(getPhoto);
    },

    selectedPhotos(photo){
      if(this.selectedPhotosList.includes(photo)){
        this.selectedPhotosList.splice(this.selectedPhotosList.indexOf(photo), 1);
      }else{
        this.selectedPhotosList.push(photo)
      }
    },

    itemsContains(n) {
      return this.selectedPhotosList.includes(n)
    },

    removePhoto(n){
      this.photos.splice(this.photos.indexOf(n), 1);
      if(this.selectedPhotosList.includes(n)){
        this.selectedPhotosList.splice(this.selectedPhotosList.indexOf(n), 1);
      }
    }, 

    dataURLtoFile(dataurl, filename) {
 
      let arr = dataurl.split(','),
          mime = arr[0].match(/:(.*?);/)[1],
          bstr = atob(arr[1]), 
          n = bstr.length, 
          u8arr = new Uint8Array(n);
          
      while(n--){
          u8arr[n] = bstr.charCodeAt(n);
      }        
      return new File([u8arr], filename, {type:mime});
    },

    async callImageAPI(uuid){
      const total_images= await imagesApi.getStoreObjectImages(uuid);
      let order = 1
      if(total_images.status){
        order = order + parseInt(total_images.total_count);
      }
      await this.selectedPhotosList.map(async (photo, key) => {
        const file =await this.dataURLtoFile(photo,`order-${key+order}.jpg`);
        let data = new FormData();
        data.append('path', file)
        data.append('order', key + order)
        await imagesApi.addImageToStoreObject(uuid, data)
      }); 
    },

    // Get the UUID from QR Scan
    async onDecode (currentUUID) {
      console.log("DECODE", currentUUID)
      this.currentUUID = currentUUID
      if(this.currentUUID !== ''){
        const storedObjectData = await storeObjectApi.getStoreObjectByUUID(currentUUID)
        if(storedObjectData.status){
          const currentUUID = this.currentUUID
          const previousUUID = this.previousUUID
          if (previousUUID !== '' && storedObjectData.data.nestable){
            console.log("MAKE RELATION")
            const nestableData = {
              'holdingUUID': previousUUID,
              'containingUUID': currentUUID
            }
            await nestableObjectApi.createNestableObject(nestableData)
          }
          // Attach Images
          if(this.selectedPhotosList.length > 0){
            await this.callImageAPI(this.currentUUID)
            this.photos = this.photos.filter(x => !this.selectedPhotosList.includes(x))
            this.selectedPhotosList = []
          }
          this.getStoredObjectImages(currentUUID)  
        }else{
          this.previousUUID = currentUUID
          this.createObject = true
        }
      }
    },

    // Start function for scanning QR
    async onInit (promise) {
      console.log("INIT")
      try {
        await promise
      } catch (error) {
        if (error.name === 'NotAllowedError') {
          this.error = "ERROR: you need to grant camera access permisson"
        } else if (error.name === 'NotFoundError') {
          this.error = "ERROR: no camera on this device"
        } else if (error.name === 'NotSupportedError') {
          this.error = "ERROR: secure context required (HTTPS, localhost)"
        } else if (error.name === 'NotReadableError') {
          this.error = "ERROR: is the camera already in use?"
        } else if (error.name === 'OverconstrainedError') {
          this.error = "ERROR: installed cameras are not suitable"
        } else if (error.name === 'StreamApiNotSupportedError') {
          this.error = "ERROR: Stream API is not supported in this browser"
        }
      }
    },

    cameraMode() {
      setTimeout(() => {
          this.video = document.querySelector('#video');
          if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          navigator.mediaDevices.getUserMedia({ video: { width: { ideal: 1280 }, height: { ideal: 720}}, audio: false }).then(stream => {
              this.video.srcObject = stream;
          });
          }
      }, 300);
    },

    // Reset the form Data
    resetForm(){
      this.$refs.uuid.reset()
      this.$refs.type.reset()
      this.$refs.name.reset()
      this.$refs.description.reset()
      this.$refs.purpose.reset()
      this.$refs.nestable.reset()
      this.$refs.completed.reset()
      this.$refs.owningEntity.reset()
      this.$refs.locationEntityUUID.reset()
      this.$refs.visibility.reset()
      this.$refs.quantity.reset()
      this.$refs.category.reset()
      this.$refs.standarisedObject.reset()
    },

    // Open a form for create store object
    createStoreObject() {
      this.addObject = true    
      this.create = true    
    },

    // Open a from after scan QR
    async createStoreObjectWithUUID(){
      this.form.uuid = this.currentUUID
      this.addObject = true 
      this.createObject = false
      this.create = false
      await storeObjectApi.addStoreObject(this.form); 
      // Attach Images
      if(this.selectedPhotosList.length > 0){
        await this.callImageAPI(this.currentUUID)
        this.photos = this.photos.filter(x => !this.selectedPhotosList.includes(x))
        this.selectedPhotosList = []
      }
    },
    
    // Close the create store object form
    closeCreateForm(){
      this.addObject = false
      this.resetForm()
    },

    // Keep track of changed value and add it into form data
    changeInputValue(event, name, isNumber){
      if(isNumber && (name === 'completed' || name === "nestable")){
        this.form[name] = Boolean(event)
      }else if(isNumber && event === ''){
        this.form[name] = null
      }else{
        this.form[name] = event
      }
    },

    // Save Store Object
    async saveStoreObject(){
      this.addObject = false
      if(this.create){
        console.log("CREATE")
        await storeObjectApi.addStoreObject(this.form);
      }else{
        console.log("UPDATE")
        await storeObjectApi.updateStoreObjectByUUID(this.currentUUID, this.form)
      }
      // this.message = added.message
      // this.snackbar = true
      this.resetForm()
    },

    // Get all StoreObject
    async BrowseMode() {
      this.storeObject= await storeObjectApi.getStoreObject();
      this.storeObject = this.storeObject.data
    },

    // Go to particular object page
    async getStoredObjectImages(uuid){
      if(this.selectedPhotosList.length > 0){
        await this.callImageAPI(uuid)
        this.photos = this.photos.filter(x => !this.selectedPhotosList.includes(x))
        this.selectedPhotosList = []
      }
      this.$router.push({name: 'Images', params:{"uuid": uuid}})
    }
  },           
};
</script>

<style>
#scaleVideo {
  transform-origin: left top;
  transform: scale(calc(300/510)); 
  /* 300/720 */
}
#labels {
  position: absolute;
  margin: 1.5em;
  right: 0;
  top: 0;
}

.v-sheet {
  position: relative;
}

.v-toolbar{
  box-shadow: none !important;
}

.theme--light.v-toolbar.v-sheet {
    background-color: #03fcf0 !important;
}

.v-card__subtitle, .v-card__text, .v-card__title {
  padding: 0px !important;
}

.theme--dark.v-sheet {
    color: #000000 !important;
}

.space-for-bottom{
  margin-bottom: 50pt;
}

.p-10 {
  padding: 10px !important;
}

.m-b-0 {
  margin-bottom: 0px !important;
}

.preview-image{
  border-style: none !important;
}

.preview-selected-image{
  border-style: dashed !important;
  border-color: #03fcf0 !important;
}

.overlay[data-v-1f90552a], .tracking-layer[data-v-1f90552a] {
    position: inherit !important;
}

.camera[data-v-1f90552a], .pause-frame[data-v-1f90552a] {
  display: block;
  -o-object-fit: cover;
  object-fit: cover;
  width: auto !important;
  height: auto !important;
  margin-left: 15px;
}

.custom-button-delete {
    border-radius: 25px;
    min-width: 10px !important;
    height: 22px !important;
    padding: 0px 0px !important;
    margin-top: -240px;
    margin-left: 80px;
    background-color: #ff5252 !important;
    color: #FFFFFF !important;
}
</style>
