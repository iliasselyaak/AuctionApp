<template>
    <div>
        <h1 class="font-bold text-3xl p-12">Your Profile</h1>
        <div class="content flex">
            <img class="border w-52 h-52 mx-10 mb-5" v-bind:src=source alt=""/>
            <div>
                <label class="font-bold" for="image" >Change Profile</label><br>
                <input @change="onFileSelected" class="content flex my-5" type="file" name="item_img">
                <button @click="uploadImage" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="button">Change</button>
            </div>
        </div>
        <form>
        <label for="email" class="font-bold mx-10 ">Email:</label>
        <input class="border ml-10" type="email" v-model=email required>
        <label for="dob" class="font-bold mx-10" type="text" >Date of Birth:</label>
        <input class="border ml-10" type="date" v-model=dob required>
        <div class="m-10">
            <label class="font-bold" for="item" >Change info:</label><br>
            <button @click="changeProfile" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="button">Change</button>
        </div>
    </form>
    </div>
</template>

<script lang="ts">
import Cookies from 'js-cookie'
import { defineComponent} from 'vue'

export default defineComponent({
    data(){
        return{
            email:"",
            source:"",
            dob:""
        }
    },
    methods: {
        async profile(){
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
            this.username= await response.json();
            this.email = this.username.email
            this.dob = this.username.dob
            console.log(this.username)
        },
        async changeProfile(){
            let response = await fetch("http://localhost:8000/changeprofile/",{
                method: "PUT",
                headers: new Headers({
                    "Content-Type": "application/json",
                    "X-CSRFToken": ""+ Cookies.get('csrftoken'),
                    credentials: "include",
                    referrerPolicy: "no-referrer",
                }),
                body: JSON.stringify({email:this.email , dob:this.dob}),
            });
            
            const data = await response.json();
        },
        onFileSelected(event: any){
            this.selectedFile = event.target.files[0]
        },
        async uploadImage(){
            let formData = new FormData();
            formData.append('image', this.selectedFile)

            const response = await fetch("http://localhost:8000/api/change_image/",{
                  method:'POST',
                  headers: new Headers({
                "X-CSRFToken": ""+ Cookies.get('csrftoken'),
                credentials: "include",
                }),
                  body: formData,
            })
            .then(response => response.json())
              .then(data => {
              this.source = data
              console.log(this.source)
            })
            .catch(error => {
              console.error(error)
            });
            this.fetchImage();
        },
        async fetchImage(){
            let response = await fetch("http://localhost:8000/api/getimage/", {
                method: "GET",
                headers: new Headers({
                    "Content-Type": "application/json",
                    "X-CSRFToken": ""+ Cookies.get('csrftoken'),
                    credentials: "include",
                    referrerPolicy: "no-referrer",
                })
            });
            const data = await response.json();
            this.source= data.url
        }
    },
    created(){
        this.profile();
        this.fetchImage();
    }
})
</script>
