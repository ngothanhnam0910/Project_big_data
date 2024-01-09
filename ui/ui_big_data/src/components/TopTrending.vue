<script setup>
import {Row, Col, Card, RangePicker, Skeleton} from 'ant-design-vue';
import {
    UserOutlined, MenuFoldOutlined, MenuUnfoldOutlined
    
} from '@ant-design/icons-vue';

import axios from 'axios';
import { ref } from 'vue';
const value1 = ref();
let last10Twitter = [];
let topPair = [];
let isLoading = ref(true);
axios.get(`http://localhost:5000/get_overview`)
    .then(response => {
      response.data.symbols.forEach(item => {
        topPair.push({label: item.symbol, y: item.tweet_count})
      });


      last10Twitter = response.data.tweets;
      isLoading.value = false
    })

let getByRange = async (starttime, endtime)=> {
  console.log(value1);
  if (value1) {

    await axios.get(`http://localhost:5000/get_trending_symbols?startTime=${starttime}&endTime=${endtime}`)
    .then(response => {
      console.log(response);
      topPair = [];

      response.data.symbols.forEach(item => {
        topPair.push({label: item.symbol, y: item.tweet_count})
      });


    })
  }
};

let  options = {
        animationEnabled: true,
        exportEnabled: true,
        title:{
           text: value1?"Top Trending Coins in last 10 minutes.": `Top Trending Coins in ${value1[0]}-${value1[1]}.`
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
        <div style="margin-bottom: 15px;">
          <RangePicker v-model:value="value1"  show-time/>
          <Button @click="getByRange(value1[0].toISOString(), value1[1].toISOString())">Submit</Button>
        </div>
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