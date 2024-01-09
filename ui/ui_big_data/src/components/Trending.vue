<script setup>
import {Row, Col, Card, Skeleton} from 'ant-design-vue';
import {
    UserOutlined, MenuFoldOutlined, MenuUnfoldOutlined
    
} from '@ant-design/icons-vue';
import axios from 'axios';
import { reactive, ref } from 'vue';

let last10Twitter = [];
let topPair = [];
let isLoading = ref(true);
axios.get(`http://localhost:5000/get_overview`)
    .then(response => {
      console.log(response)
      response.data.symbols.forEach(item => {
        topPair.push({label: item.symbol, y: item.tweet_count})
      });


      last10Twitter = response.data.tweets;
      console.log(last10Twitter)
      isLoading.value = false
    })

let    options = {
        animationEnabled: true,
        exportEnabled: true,
        title:{
          text: "Top Trending Coins in last 10 minutes."
        },
        axisX: {
          labelTextAlign: "right"
        },
        axisY: {
          title: "Tweet count",
          suffix: ""
        },
        data: [{
          type: "bar",
          yValueFormatString: "#,### tweets",
          dataPoints: topPair
        }]
      }
</script>
<template>
 <div v-if="isLoading == true">
<Skeleton />
 </div>
 <div v-if="isLoading == false">
  <Row>
    <Col :span="17">
      <CanvasJSChart :options="options"/>
    </Col>
    <Col :span="7">
      <div  style="height: 65vh; overflow-y: auto;">
        <div v-for="twitter in last10Twitter" >
          <Card :title="twitter.recorded_time" :bordered="false" style="width: 300px; margin-bottom: 15px; background-color:azure">
            {{ twitter.content }}
          </Card>
        </div>
      </div> 
    </Col>
  </Row>
 </div>
    
</template>

<script>
export default {
  data() {
    return {
      chart: null,
      
    }
  }
}
</script>