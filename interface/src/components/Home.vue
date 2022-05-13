<template>
  <div class="home-container">
    <img :src="logo" />
    <SearchInput ref="searchInput" @submit="onSubmit" />
    <button @click="handleSearch">Buscar</button>
  </div>
</template>

<script>
import SearchInput from "./SearchInput.vue";

export default {
  components: {
    SearchInput,
  },
  data() {
    return {
      logo: require("@/assets/logo.png"),
    };
  },
  methods: {
    handleSearch() {
      const searchInput = this.$refs["searchInput"]
      this.onSubmit(searchInput.value)
    },
    onSubmit(value) {
      if (value !== "")
        this.$router.push({
          name: "search",
          query: {
            value: value,
          },
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.home-container {
  height: 100vh;
  min-height: 500px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  > img {
    width: 350px;
    height: 180px;
    border-radius: 20px;
    margin-bottom: 50px;
  }
  > button {
    margin-top: 30px;
    width: 160px;
    height: 33px;
    border-radius: 3px;
    background-color: #ececec78;
    border: 0px;
    cursor: pointer;
    color: #353535c4;
    &:hover {
      box-shadow: 0px 0px 3px #b7b7b7;
    }
  }
}
</style>
