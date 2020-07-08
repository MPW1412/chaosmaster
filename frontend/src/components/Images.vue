<template>
  <div>
    <v-app-bar>    
      
       <v-btn small 
        id="#back"
        v-on:click="goToObjects">
        GO BACK
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn small class="ma-2"
        id="#addImage"
        v-on:click="editObjectForm">
        Edit Object
      </v-btn>
      <v-btn small class="ma-2"
        id="#addImage"
        v-on:click="addImageForm">
        Add Images
      </v-btn>
    </v-app-bar>

    <v-container>
      <v-row no-gutters v-if="images.length > 0">
        <v-col
            v-for="n in images"
            :key="n.id"
            class="p-10"
            cols="12"
            sm="4">
            <v-layout>
                <v-flex>
                  <v-card>
                      <v-img :src="n.image_url" name="test" height="200px">
                      </v-img>
                      <v-card-title primary-title class="v-card-margin-left">
                        <div>
                            <h3 class="headline mb-0">
                              <v-row>
                                <v-col sm="10" cols="10">
                                  Order: {{n.order}}
                                </v-col>
                                <v-col sm="2" cols="2" >
                                  <v-btn text color="error"
                                    v-on:click="deleteConfirmation(n.id)">
                                    <v-icon>mdi-delete</v-icon>
                                  </v-btn>
                                </v-col>
                              </v-row>
                            </h3>
                            <div></div>
                        </div>
                      </v-card-title>
                  </v-card>
                </v-flex>
            </v-layout>
        </v-col>
      </v-row>
      <v-row v-else>
        NO IMAGES AVAILABLE
      </v-row>
    
    </v-container>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" persistent max-width="290">
        <v-card class="dialog-custom">
          <div class="p-25">
            <v-card-title class="headline">Are You Sure?</v-card-title>
            <v-card-text>You want delete this?</v-card-text>
          </div>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" 
              @click="dialog = false">
              NO
            </v-btn>
            <v-btn color="green" 
              v-on:click="deleteImage">
              YES
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
    <!-- <v-form method="post" id="nativeForm"> -->
    <v-layout row justify-center>
      <v-dialog v-model="addForm" persistent max-width="600px">
        <v-card class="v-card-images">
          <v-card-title>
            <span class="headline">Add Images</span>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12>
                    <v-file-input accept="image/*" label="Upload Image File*"
                    @change="changeOrder($event,'imageFile')"
                    :rules="imageRules"
                    prepend-icon="mdi-camera"
                    ref="image">
                  </v-file-input>
                </v-flex>
                <v-flex xs12>
                  <v-text-field label="Order Number*"  
                    @change="changeOrder($event,'orderNumber')"
                    :rules="orderRules"
                    v-model="orderNumber"
                    hide-details="auto"
                    ref="order">
                  </v-text-field>
                </v-flex>               
              </v-layout>
            </v-container>
            <small>*indicates required field</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text v-on:click="closeForm">Close</v-btn>
            <v-btn color="blue darken-1" text 
              v-on:click="addImage">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
    <!-- </v-form> -->
     <v-layout row justify-center>
      <v-dialog v-model="editObject" fullscreen transition="dialog-bottom-transition">
        <v-card class="v-card-images">
          <v-toolbar color="#03fcf0">
            <v-btn icon @click="editObject = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>Edit Object</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn small class="ma-2"
                id="#saveBtn"
                v-on:click="editStoreObject">
              Save
            </v-btn>
          </v-toolbar>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12 sm5>
                  <v-text-field label="UUID" hide-details="auto"
                    :value="uuid"
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
                  :value="form.type"
                  label="Type"
                  @change="changeInputValue($event,'type', false)"
                ></v-select>
                </v-flex>
                <v-flex xs12>
                  <v-text-field label="Name" hide-details="auto"
                    @change="changeInputValue($event,'name', false)"
                    :value="form.name"
                    :rules="nameRules">
                  </v-text-field>
                </v-flex>
                 <v-flex xs12>
                  <v-text-field label="Description" hide-details="auto"
                    @change="changeInputValue($event,'description', false)"
                    :value="form.description">
                  </v-text-field>
                </v-flex>      
                <v-flex xs12>
                  <v-text-field label="Purpose" hide-details="auto"
                    @change="changeInputValue($event,'purpose', false)"
                    :value="form.purpose">
                  </v-text-field>
                </v-flex>  
                <v-flex xs12 sm5>
                  <v-checkbox label="Nestable"
                    @change="changeInputValue($event,'nestable', true)"
                    :value="form.nestable">
                  </v-checkbox>
                </v-flex>
                <v-flex xs12 sm2>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-checkbox label="Completed"
                    @change="changeInputValue($event,'completed', true)"
                    :value="form.completed">
                  </v-checkbox>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Owning Entity" hide-details="auto"
                    @change="changeInputValue($event,'owningEntity', false)"
                    :value="form.owningEntity"
                    :rules="uuidRules">
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm2>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Location Entity UUID" hide-details="auto"
                    @change="changeInputValue($event,'locationEntityUUID', false)"
                    :value="form.locationEntityUUID"
                    :rules="uuidRules">
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Visibility" hide-details="auto"
                    @change="changeInputValue($event,'visibility', true)"
                    :value="form.visibility"
                    :rules="numberRules">
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm2>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Quantity" hide-details="auto"
                    @change="changeInputValue($event,'quantity', true)"
                    :value="form.quantity"
                    :rules="numberRules">
                  </v-text-field>
                </v-flex>
              
                 <v-flex xs12 sm5>
                  <v-text-field label="Category" hide-details="auto"
                    @change="changeInputValue($event,'category', true)"
                    :value="form.category"
                    :rules="numberRules">
                  </v-text-field>
                </v-flex>
                  <v-flex xs12 sm2>
                </v-flex>
                <v-flex xs12 sm5>
                  <v-text-field label="Standarised Object" hide-details="auto"
                    @change="changeInputValue($event,'standarisedObject', false)"
                    :value="form.standarisedObject"
                    :rules="uuidRules">
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
  </div>
</template>

<script>

import imagesApi from '../api/images';
import storeObjectApi from '../api/storedObject';

export default {
    name: 'Images',

    data(){
      return {
        uuid:'',
        images: '',
        dialog: false,
        id: '',
        snackbar: false,
        addForm: false,
        editObject: false,
        message: '',
        orderNumber: '',
        imageFile: {},
        form:{

        },
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
        orderRules: [
          v => !!v || 'Required.',
          v => (v && !isNaN(v)) || 'Order Must be Number',
        ],
        imageRules: [
          v => !!v || 'Required.'
        ],
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
      //Confirm the delte of image
      deleteConfirmation(id) {
        this.dialog = true
        this.id = id
      },

      // Delete the image from store object
      async deleteImage(){
        this.dialog = false
        const uuid = this.$route.params.uuid;
        const deleteMessage = await imagesApi.deleteImageById(this.id);
        this.message = deleteMessage.message
        this.snackbar = true
        this.images= await imagesApi.getStoreObjectImages(uuid);
        this.images = this.images.data;
      },

      // Open a image form
      addImageForm() {
        this.addForm = true
      },

      // Add image into store object
      async addImage(){
        this.addForm = false
       
        let data = new FormData();

        data.append('path', this.imageFile)
        data.append('order', this.orderNumber)

        this.orderNumber = ''
        this.imageFile = {}
        const successMessgae = await imagesApi.addImageToStoreObject(this.uuid, data)

        this.message = successMessgae.message
        this.snackbar = true

        this.images= await imagesApi.getStoreObjectImages(this.uuid);
        this.images = this.images.data;
        this.$refs.order.reset()
        this.$refs.image.reset()
      },

      // Keep track of image form data
      changeOrder(event, name){
        this[name] = event
        console.log("CHANGE",this.orderNumber, this.imageFile)
      },

      // Close the add image form
      closeForm(){
        this.$refs.order.reset()
        this.$refs.image.reset()
        this.addForm = false
      },

      // Open a form for edit store object
      async editObjectForm(){
        this.editObject = true
        const storedObjectData = await storeObjectApi.getStoreObjectByUUID(this.uuid)
        this.form = storedObjectData.data
        console.log(this.form)
      },

      // Keep track of change form data and add it into form data
      changeInputValue(event, name, isNumber){
        if(isNumber && (name === 'completed' || name === "nestable")){
          this.form[name] = Boolean(event)
        }else if(isNumber && event === ''){
          this.form[name] = null
        }else{
          this.form[name] = event
        }
      },

      // Save edit store object data 
      async editStoreObject(){
        this.editObject = false
        const updateStoreObject = await storeObjectApi.updateStoreObjectByUUID(this.uuid, this.form)
        console.log(updateStoreObject) 

        this.message = updateStoreObject.message
        this.snackbar = true
      },

      // Go to main page
      goToObjects(){
        this.$router.push({name: 'Home'})
      }
    },

    async mounted () {
        this.uuid = this.$route.params.uuid;
        this.images= await imagesApi.getStoreObjectImages(this.uuid);
        this.images = this.images.data;
    },  
};
</script>

<style>

.v-card {
    width: 250px !important;
    margin-bottom: 20px !important;
}

.v-card__actions {
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    padding: 8px 4px;
}

.v-card__actions, .card__media__content {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
}

.v-card-margin-left {
  margin-left: 20px !important;
}

.dialog-custom {
  width: 100% !important;
  margin-bottom: 0px !important;
}

.p-25{
  padding: 25px;
}
.v-card-images{
  width: 600px !important;
  margin-bottom: 0px !important;
}

.p-10 {
  padding: 10px !important;
}

</style>
