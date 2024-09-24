<template>
  <div>
    <button @click="showModal=true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="button">+Add Item</button>
    <BaseModal :show="showModal">
      <div class="p-4">
        <div>
          <label for="title">Item's Title</label><br>
          <input v-model="item_title" class="border" type="text" required>
        </div>
        <div>
          <label for="item" >Description</label><br>
          <textarea v-model="item_description" class="border" rows = "5" cols = "50" placeholder="Enter your item's description." required></textarea>
        </div>
        <div>
          <label for="image" >Image</label><br>
          <input @change="onFileSelected" ref="fileInput" type="file" name="item_img">
        </div>
        <div>
          <label for="bidEnd" >Time bid finishes</label><br>
          <input v-model="item_bid_finish" class="border" type="date" name="date">
        </div>
        <div>
          <label for="price" >Starting price</label><br>
          <input v-model="item_start_price" step='0.01' class="border" type="number" name="date">
        </div>
  
        <button type="button" class="bg-indigo-200 px-3 py-1 font-medium mx-2" @click="create_item()">
          Submit
        </button>
        <button type="button" class="bg-indigo-200 px-3 py-1 font-medium" @click="showModal = false, fetchItems">
          Hide modal
        </button>
      </div>
    </BaseModal>
  </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref} from 'vue'
  import BaseModal from './modals/BaseModal.vue'
  import Cookies from 'js-cookie';
  
  export default defineComponent({
      components: {BaseModal},
      setup(){
          const showModal = ref(false);
          return{showModal}
      },
      data() {
        return {
          item_title: "",
          item_description: "",
          item_bid_finish: "",
          item_start_price: "",
          selectedFile: "",
          owner_id: 0,
        }
      },
      methods:{
        onFileSelected(event: any){
          this.selectedFile = event.target.files[0]
        },
        async get_owner(): Promise<void> {
            // @ts-ignore
            let response = await fetch("http://localhost:8000/getuser/", {
                method: "GET",
                headers: new Headers({
                    "Content-Type": "application/json",
                    "X-CSRFToken": ""+ Cookies.get('csrftoken'),
                    credentials: "include",
                    referrerPolicy: "no-referrer",
                })
            });
            const data = await response.json();
            console.log(data.id)
            this.owner_id = data.id;
        },
        async create_item(): Promise<void> {
  
          const headers = new Headers({
              "Content-Type": "application/json",
              "X-CSRFToken": Cookies.get('csrftoken')
              } as HeadersInit);
  
          console.log(this.get_owner())
          await this.get_owner()
          const response = await fetch("http://localhost:8000/api/items/", {
                  method: 'POST',
                  headers: headers,
                  body: JSON.stringify(
                    {
                      title: this.item_title,
                      description: this.item_description,
                      bid_time_finish: this.item_bid_finish,
                      start_bid: this.item_start_price,
                      owner: this.owner_id,
                    }
                  ),
                  credentials: "include",
                  mode: "cors",
                  referrerPolicy: "no-referrer",
              });
            const data = await response.json();
            let id = data.id
            let formData = new FormData();

            formData.append('image', this.selectedFile)
            const responseImg = await fetch("http://localhost:8000/api/item_image/" + id+'/',{
                  method:'POST',
                  headers: new Headers({
                "X-CSRFToken": ""+ Cookies.get('csrftoken'),
                credentials: "include",
                }),
                  body: formData,

  
            })
            .then(response => response.json())
              .then(data => {
              console.log(data)
            })
            .catch(error => {
              console.error(error)
            });

            this.showModal = false;
            this.fetchItems();
        },
        async fetchItems(): Promise<void> {
              // Perform an Ajax request to fetch the list of items
              let response = await fetch("http://localhost:8000/api/items/",
              {
                  credentials: "include",
                  mode: "cors",
                  referrerPolicy: "no-referrer",
    
              });
              let data = await response.json();
              this.$emit('child-method',data)
          },
      },
  })
  </script>
  
  