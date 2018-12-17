<template>

<div>
<h1>{{ header }}</h1>

<ul id="task-list">
  <li v-for="item in items">
    {{ item.message }}
  </li>
</ul>

</div>
</template>

<script>
export default {
  name: 'Index',
  data () {
    return {
      header: 'Welcome to Media parse',
      items:[
        { message: 'Foo' },
        { message: 'Bar' },
        { message: 'Bar' }
      ]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
