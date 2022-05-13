import VueRouter from "vue-router";
import Home from "@/components/Home";
import Search from "@/components/Search";
import Document from "@/components/Document";
import Vue from "vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/search",
    name: "search",
    component: Search,
  },
  {
    path: "/document/id/:id",
    name: "document",
    component: Document,
  },
  {
    path: "*",
    redirect: { name: "home" },
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
