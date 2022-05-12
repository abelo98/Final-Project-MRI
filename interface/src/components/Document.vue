<template>
  <div class="body">
  {{ text }}
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: ""
    }
  },
  created() {
    let id = this.$route.params.id
    this.getDocument(id)
  },
  methods: {
    async getDocument(id) {
      try {
        const data = await fetch(`http://127.0.0.1:8000/document/${id}`);
        let body = JSON.parse(await data.text());
        this.text = body.text
      } catch (err) {
        console.log(err);
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.body {
  text-align: left;
  padding: 30px;
  font-size: 20px;
  white-space: pre-wrap;
}
</style>
