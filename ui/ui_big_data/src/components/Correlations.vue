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
  import btcData from "../assets/btcusd2018.json";
  import CanvasJS from '@canvasjs/stockcharts';
  export default {
    data() {
      var dps1 = [], dps2 = [], dps3 = [];
      btcData.forEach(data => {
        dps1.push({ x: new Date(data["date"]), y: [data["open"], data["high"], data["low"], data["close"]] });
        dps2.push({ x: new Date(data["date"]), y: data["volume_usd"] });
        dps3.push({ x: new Date(data["date"]), y: data["close"] });
      });
      return {
        chart: null,
        options: {
          theme: "light2",
          exportEnabled: true,
          title: {
            text: "Coin Price/ Mentions"
          },
          charts: [{
            toolTip: {
              shared: true
            },
            axisX: {
              lineThickness: 5,
              tickLength: 0,
              labelFormatter: function(e) {
                return "";
              }
            },
            axisY: {
              prefix: "$"
            },
            legend: {
              verticalAlign: "top"
            },
            data: [{
              showInLegend: true,
              name: "Coin Price (in USDT)",
              yValueFormatString: "$#,###.##",
              type: "candlestick",
              dataPoints: dps1
            }]
          }, {
            height: 80,
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
          }],
          navigator: {
            data: [{
              dataPoints: dps3
            }],
            slider: {
              minimum: new Date(2018, 6, 1),
              maximum: new Date(2018, 8, 1)
            }
          }
        },
        styleOptions: {
          width: "100%",
          height: "420px"
        }
      }
    },
    methods: {
      addSymbols(e) {
        var suffixes = ["", "K", "M", "B"];
        var order = Math.max(Math.floor(Math.log(Math.abs(e.value)) / Math.log(1000)), 0);
        if (order > suffixes.length - 1) order = suffixes.length - 1;
        var suffix = suffixes[order];
        return CanvasJS.formatNumber(e.value / Math.pow(1000, order)) + suffix;
      }
    }
  }
</script>
