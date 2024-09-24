<template>
  <div class="font-sans">
    <AddItem v-on:child-method="updateItems"/>
    <div>
        <div class="font-sans text-black bg-white flex my-10 justify-center">
            <div class="border rounded overflow-hidden flex">
                <input v-model="search" type="text" class="pl-4 py-2 pr-96" placeholder="Search...">
                <button @click=fetchItems() class="flex items-center justify-center px-4 border-l">
                    <svg class="h-4 w-4 text-grey-dark" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M16.32 14.9l5.39 5.4a1 1 0 0 1-1.42 1.4l-5.38-5.38a8 8 0 1 1 1.41-1.41zM10 16a6 6 0 1 0 0-12 6 6 0 0 0 0 12z"/></svg>
                </button>
            </div>
        </div>
    </div>
    <h1 class="font-bold text-3xl px-12">Items Listing</h1>
    <div v-for="item in filtered_items">
        <Item v-on:child-method="updateItems" :item=item />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Item from './Item.vue';
import NavBar from './NavBar.vue';
import AddItem from './AddItem.vue';
import SearchBar from './SearchBar.vue';
import Cookies from 'js-cookie';

export default defineComponent({
    components: { NavBar, SearchBar, Item, AddItem},
    data() {
        return{
            search: "",
            items: [],
            filtered_items: [],
        }
    },
    methods: {
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
            this.filtered_items = this.items.filter((item: {title: string, description: string}) => (item.title.indexOf(this.search) !== -1) || (item.description.indexOf(this.search) !== -1))
            console.log(this.items);
            console.log(this.filtered_items)
            this.$forceUpdate()
        
        },
        updateItems() {
            this.fetchItems();
            console.log("Hello")
        }
    },
    created() {
        this.fetchItems();
    },
})
</script>

