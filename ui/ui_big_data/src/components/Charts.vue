<!-- App.vue -->
<script setup>
import {Row, Col, Card, Button, Input} from 'ant-design-vue';
import {
    UserOutlined, MenuFoldOutlined, MenuUnfoldOutlined
    
} from '@ant-design/icons-vue';
</script>
<template>
  <div style="display: flex; flex-direction: row; align-items: center; justify-content: end; margin-bottom: 25px;">
    <Input type="text" v-model="this.pair" placeholder="Search" style="width: 200px; margin-right: 10px;"></Input>
    <Button>Submit</Button>
  </div>
  <CanvasJSStockChart :options="this.options" :style="this.styleOptions" />
</template>

<script>
import msftData from "../assets/msft2020.json";
  export default {
    data() {
      var dps1 = [], dps2 = [];
      msftData.forEach(data => {
        dps1.push({ x: new Date(data["date"]), y: [data["open"], data["high"], data["low"], data["close"]] });
        dps2.push({ x: new Date(data["date"]), y: data["close"] });
      });
      return {
        chart: null,
        pair: '',
        options: {
          exportEnabled: true,
          theme: "light2",
          title: {
            text: `Number of tweets/sentiment`
          },
          subtitles: [{
            text: ""
          }],
          charts: [{
            height: 130,
            toolTip: {
              shared: true
            },
            axisY: {
              prefix: "$",
              labelFormatter: this.addSymbols
            },
            legend: {
              verticalAlign: "top"
            },
            data: [{
              showInLegend: true,
              name: "Number of mentions",
              yValueFormatString: "#,###.##",
              dataPoints: dps2
            }]
          },
          {
            height: 130,
            toolTip: {
              shared: true
            },
            axisY: {
              prefix: "$",
              labelFormatter: this.addSymbols
            },
            legend: {
              verticalAlign: "top"
            },
            data: [{
              showInLegend: true,
              name: "Sentiment",
              yValueFormatString: "#,###.##",
              dataPoints: dps2
            }]
          }],
          navigator: {
            data: [{
              dataPoints: dps2
            }],
            slider: {
              minimum: new Date(2020, 1, 1),
              maximum: new Date(2020, 11, 1)
            }
          }
        },
        styleOptions: {
          width: "100%",
          height: "400px"
        }
      }
    }
  }
</script>