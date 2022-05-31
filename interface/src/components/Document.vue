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

        // console.log(`document id ${id}`);
        //
        // this.text = "Akodon spegazzinii, also known as Spegazzini's akodont[4] or Spegazzini's grass mouse,[1] is a rodent in the genus Akodon found in northwestern Argentina. It occurs in grassland and forest at 400 to 3,500 m (1,300 to 11,500 ft) above sea level. After the species was first named in 1897, several other names were given to various populations now included in A. spegazzinii. They are now all recognized as part of a single, widespread and variable species. Akodon spegazzinii is related to Akodon boliviensis and other members of the A. boliviensis species group. It reproduces year-round. Because it is widely distributed and common, Akodon spegazzinii is listed as \"least concern\" on the IUCN Red List.\n" +
        //     "\n" +
        //     "Akodon spegazzinii is medium in size for the A. boliviensis species group. The coloration of its upperparts varies considerably, from light to dark and from yellowish to reddish brown. The underparts are yellow-brown to gray. The eyes are surrounded by a ring of yellow fur. The skull contains an hourglass-shaped interorbital region (between the eyes) and various features of the skull distinguish the species from its close allies. Head and body length is 93 to 196 mm (3.7 to 7.7 in) and body mass is 13.0 to 38.0 g (0.46 to 1.34 oz). Its karyotype has 2n = 40 and FN = 40.[";
        //
        // this.text += this.text;
        // this.text += this.text;
        // this.text += this.text;

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
