<template>
  <div class="search">
    <img v-if="!fromSearch" :src="searchImg" />
    <input v-model="value" @keydown.enter="onSubmit" />
    <img v-if="fromSearch" :src="searchImg" style="margin-left: 10px; cursor: pointer" @click="onSubmit" />
  </div>
</template>

<script>
export default {
  props: {
    fromSearch: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchImg: require("@/assets/search.svg"),
      value: ""
    }
  },
  methods: {
    onSubmit() {
      this.$emit("submit", this.value)
    },
    setValue(value) {
      this.value = value
    }
  }
}
</script>

<style lang="scss" scoped>
.search {
  box-shadow: 1px 1px 2px 0px #3535351c;
  display: flex;
  align-items: center;
  border: 1px solid #ebebeb;
  border-radius: 20px;
  width: fit-content;
  padding: 5px 10px 5px 10px;
  transition: border 0.3s;
  &:focus-within {
    border: 1px solid #3535353b;
  }
  > img {
    width: 20px;
    height: 20px;
  }
  > input {
    margin-left: 10px;
    margin-bottom: 3px;
    color: #353535;
    font-family: Roboto;
    font-size: 15px;
    width: 470px;
    height: 26px;
    border: 0px;
    &:focus {
      outline: 0ch;
    }
  }
}
</style>
