<template>
    <div>
        <img @click="showModal = true" src="../assets/text.png" class="w-8 h-8 mx-60 cursor-pointer">
        <BaseModal :show="showModal">
        <div class="p-4">
            <div v-for="message in messages_to_display">
                {{message}}
            </div>
            <div>
                <label for="item" >Message</label><br>
                <textarea v-model="message_text" class="border" rows = "5" cols = "50" placeholder="Enter message." required></textarea>
            </div>
            <button type="button" class="bg-indigo-200 px-3 py-1 font-medium mx-2" @click="post_message()">
            Submit
            </button>
            <button type="button" class="bg-indigo-200 px-3 py-1 font-medium" @click="showModal = false">
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
    created() {
        this.fetchItems()
    },
    props: ["item"],
    components: {BaseModal},
    data () {
        return{
            messages: [],
            message_text: "",
            sender_id: 0,
            messages_to_display: [],
        }
    },
    setup () {
        const showModal = ref(false);
        return{showModal}
    },
    methods: {
        created() {
            this.fetchItems()
            
        },
        async get_sender(): Promise<void> {
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
            this.sender_id = data.id;
        },
        async post_message(): Promise<void> {
            await this.get_sender();
            console.log({
                    text: this.message_text,
                    sender: this.sender_id,
                    receiver: this.item.owner_id,
                    item: this.item.id})
            let response = await fetch("http://localhost:8000/api/messages/",
            {
                method: "POST",
                headers: new Headers({
                    "X-CSRFToken": ""+ Cookies.get('csrftoken'),
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                    }),
                body: JSON.stringify({
                    text: this.message_text,
                    sender: this.sender_id,
                    receiver: this.item.owner_id,
                    item: this.item.id})
            });
            this.fetchItems()
        },
        async fetchItems(): Promise<void> {
            // Perform an Ajax request to fetch the list of items
            let response = await fetch("http://localhost:8000/api/messages/",
            {
                headers: new Headers({
                "X-CSRFToken": ""+ Cookies.get('csrftoken'),
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                })
            });
            let data = await response.json();
            this.messages = data.messages.filter((message: {
                id: number,
                text: string,
                time_sent: string, 
                sender_id: number, 
                sender: string, 
                recipient_id: number, 
                recipient: string, 
                item_id: number,
                item: string,        
            }) => message.item_id == this.item.id);
            this.questions_message()
        },
        questions_message(): void {
            this.messages_to_display = []
            this.messages.forEach((message: {
                id: number,
                text: string,
                time_sent: string, 
                sender_id: number, 
                sender: string, 
                recipient_id: number, 
                recipient: string, 
                item_id: number,
                item: string,        
            })=>{
                this.messages_to_display.push(`${message.sender}: ${message.text}`);
            });
            
        }
    },
})
</script>
