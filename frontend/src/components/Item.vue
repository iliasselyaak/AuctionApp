<template>
    <!-- <div v-for="item in items"> -->
        <div class="content flex mx-20 mt-20">
            <img class="border w-96 h-52" :src=item.image alt="">
            <div class="px-4">
                <div class="content flex">
                    <h1 class="font-bold text-lg w-96">{{item.title}}</h1>
                    <Message :item=item />
                </div>
                <p class="text-gray-600 h-20">{{item.description}}</p>
                <h3>Top Bidder: {{item.last_bidder}}</h3>
                <h3>Seller: {{item.owner}}</h3>
                <div class="content flex mb-20">
                    <h3 class="py-2 pr-40">{{getRemainingTime(item.bid_time_finish)}}</h3>
                    <button @click="placeBid(item)" class="bg-nav-blue hover:bg-blue-700 text-white font-bold py-2 px-6 mr-3 -my-2 rounded-full">Place Bid</button>
                    <input v-model="enteredBid" type="text" class="w-12 border rounded">
                    <h1 class="font-bold text-3xl pl-10">£{{item.bid}}</h1>
                </div>
            </div>
            <hr class="mx-10">
        </div>
    <!-- </div> -->
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Message from './Message.vue';
import Cookies from 'js-cookie';

export default defineComponent({
    created() {
        this.fetchItems()
    },
    props: ["item"],
    setup() {
        return {};
    },
    data() {
        return {
            enteredBid: 0,
            items: [],
            bidder_id: 0,
        }
    },
    components: { Message },
    methods: {
        async get_bidder(): Promise<void> {
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
            this.bidder_id = data.id;
        },
        async fetchItems(): Promise<void> {
            // Perform an Ajax request to fetch the list of items
            let response = await fetch("http://localhost:8000/api/items/",
            {
                headers: new Headers({
                "X-CSRFToken": ""+ Cookies.get('csrftoken'),
                credentials: "include",
                mode: "no-cors",
                referrerPolicy: "no-referrer",
            })
  
            });
            let data = await response.json(); 
            this.items = data.items;
        },
        async placeBid(item: {id: number, startbid: string, bid: string, title: string, description: string, image: string, bid_time_finish: string, bought: boolean, owner_id: number, owner: string, last_bidder_id: number, last_bidder: string}): Promise<void>{
            console.log(Number(item.bid).toFixed(2))
            console.log(Number(this.enteredBid).toFixed(2))

            item.bid=String((Number(item.bid)+Number(this.enteredBid)).toFixed(2))
            await this.get_bidder()
            item.last_bidder_id = this.bidder_id
            const headers = new Headers({
            "Content-Type": "application/json",
            "X-CSRFToken":""+ Cookies.get('csrftoken')
            } as HeadersInit);

            const response = await fetch("http://localhost:8000/api/items/", {
                method: 'PUT',
                headers: headers,
                body: JSON.stringify(item),
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            });
            const data = await response.json();
            this.$emit('child-method',data)
        },
        async deleteItem(id: number): Promise<void>{
            const headers = new Headers({
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get('csrftoken')
            } as HeadersInit);

            const response = await fetch("http://localhost:8000/api/items/", {
                method: 'DELETE',
                headers: headers,
                
                body: JSON.stringify({id: id}),
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
            });
            const data = await response.json();
            this.$emit('child-method',data)
            this.fetchItems()
        },
        getRemainingTime(finish_time: string): string {
            const currentTime = new Date().getTime();
            const difference = Math.abs(new Date(finish_time).getTime() - currentTime)
            if(difference > (1000))
            {
                if(difference > (1000))
                {
                    if(difference > (1000 * 60))
                    {
                        if(difference > (1000 * 60* 60))
                        {
                            if(difference > (1000 * 60 * 60 * 24))
                            {
                                if(difference > (1000 * 60 * 60 * 24 * 7))
                                {
                                    return `${String(Math.ceil(difference / (1000 * 60 * 60 * 24 * 7)))} weeks remaining`
                                }
                                return `${String(Math.ceil(difference / (1000 * 60 * 60 * 24)))} days remaining`
                            }
                            return `${String(Math.ceil(difference / (1000 * 60 * 60)))} hours remaining`
                        }
                        return `${String(Math.ceil(difference / (1000 * 60)))} minutes remaining`
                    }
                    return `${String(Math.ceil(difference / (1000)))} seconds remaining`
                }
            }
            return "invalid date"
        }
    }
})
</script>
