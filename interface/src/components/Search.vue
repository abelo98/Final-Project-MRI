<template>
  <div class="search-container">
    <div v-if="loading" class="loader">
      <img :src="searchLoad"/>
    </div>
    <div class="header">
      <img :src="logo" @click="goToHome" style="cursor: pointer"/>
      <SearchInput ref="searchInput" from-search @submit="onSubmit"/>
      <input style="margin-left: 20px" type="checkbox" v-model="vectorialModel"> Use Vectorial Model

      <v-select
          style="margin-left:20px; border-radius: 1px"
          v-model="selected"
          :options="options"/>
    </div>
    <div class="body">
      <h5 v-if="this.vectorialModel && suggestionsQueries.length > 0">
        Quizá quisiste decir: {{ suggestionsQueries.join(". ") }}
      </h5>
      <div v-for="doc in documents" :key="doc.id" class="document-retrieve">
        <div class="content">
          <div class="text-content">
            <router-link
                :to="{ name: 'document', params: { id: doc.id }}"
                target="_blank"
                @click.prevent="openDocument(doc.id)"
            >
              Open document
            </router-link>
            <p class="text-preview">{{ doc.subject }}</p>
          </div>
        </div>
        <div class="doc-metrics">
          <img :src="likeImg" class="like" @click="setFeedback(doc.id, 1)"/>
          <p class="ranking">-</p>
          <img
              :src="dislikeImg"
              class="dislike"
              @click="setFeedback(doc.id, -1)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchInput from "./SearchInput";

export default {
  components: {
    SearchInput,
  },
  data() {
    return {
      loading: false,
      searchLoad: require("@/assets/search_load.svg"),
      logo: require("@/assets/logo.png"),
      likeImg: require("@/assets/like.svg"),
      dislikeImg: require("@/assets/dislike.svg"),
      documents: [],
      vectorialModel: true,
      options: ['CRAN CORPUS', 'MED CORPUS', '20NEWSGROUP CORPUS'],
      selected: this.$route.params.corpus,
      suggestionsQueries: []
    };
  },
  mounted() {
    const value = this.$route.query.value;
    this.getDocuments(value);
    this.$refs["searchInput"].setValue(value);
  },
  methods: {
    goToHome() {
      this.$router.push({name: "home"});
    },
    onSubmit(value) {
      if (value === "") return;
      this.$router.push({name: "search", query: {value}});
      this.getDocuments(value);
    },
    async getDocuments(value) {
      this.loading = true;
      try {

        const url = this.vectorialModel
            ? `http://127.0.0.1:8000/vect/query?value=${value}&corpus=${this.selected}`
            : `http://127.0.0.1:8000/bool/query?value=${value}&corpus=${this.selected}`;

        const data = await fetch(url);
        let body = JSON.parse(await data.text());
        this.documents = body;

        if (this.vectorialModel) {
          const suggestions = await fetch(`http://127.0.0.1:8000/query/similar?query=${value}`)
          this.suggestionsQueries = JSON.parse(await suggestions.text())
        }


      } catch (err) {
        console.log(`Error ${err}`);
      }
      this.loading = false
    }
    ,
    async setFeedback(docId, value) {
      try {
        let headers = new Headers()
        headers.append("Content-type", "application/json")
        let body = JSON.stringify({
          type: value,
          query: ""
        });
        const data = await fetch(`http://127.0.0.1:8000/feedback/${docId}`, {
          method: "PUT",
          body,
          headers
        });
        let response = JSON.parse(await data.text());
        console.log(response);
      } catch (err) {
        console.log(err);
      }
    }
    ,
    openDocument(id) {
      this.$router.push({name: "document", params: {id}});
    }
    ,
  }
}
;
</script>

<style lang="scss" scoped>
.search-container {
  p {
    margin: 0px;
  }

  .loader {
    position: absolute;
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    background: #ffffff82;

    img {
      width: 60px;
      height: 60px;
    }
  }

  .header {
    padding: 25px 20px 20px 20px;
    box-shadow: 0px 0px 3px #b7b7b7;
    display: flex;
    align-items: center;

    > img {
      width: 70px;
      height: 40px;
      border-radius: 5px;
      margin-right: 30px;
    }
  }

  .body {
    display: flex;
    flex-direction: column;

    .document-retrieve {
      display: flex;
      justify-content: space-between;
      padding: 20px 40px 20px 40px;
      border-bottom: 1px solid #ebebeb;

      .content {
        display: flex;
        align-items: center;
        width: calc(100% - 160px);

        .index {
          background: #353535;
          width: fit-content;
          padding-left: 8px;
          padding-right: 8px;
          height: 24px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 4px;

          p {
            font-weight: 500;
            font-size: 14px;
            color: white;
          }
        }

        .text-content {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          padding-right: 50px;
          padding-left: 40px;

          .text-preview {
            text-align: left;
            margin-top: 10px;
          }
        }
      }

      .doc-metrics {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: fit-content;

        img {
          width: 50px;
          height: 50px;
          cursor: pointer;
        }

        .like {
          &:hover {
            transition: transform, 0.2s;
            transform: rotate(10deg);
          }
        }

        .dislike {
          transform: rotate(180deg);

          &:hover {
            transition: transform, 0.2s;
            transform: rotate(170deg);
          }
        }
      }
    }
  }
}
</style>
