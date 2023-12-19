<script setup>
import {Row, Col, Card} from 'ant-design-vue';
import {
    UserOutlined, MenuFoldOutlined, MenuUnfoldOutlined
    
} from '@ant-design/icons-vue';
</script>
<template>
  <Row>
    <Col :span="17">
      <CanvasJSChart :options="this.options"/>
    </Col>
    <Col :span="7">
      <div  style="height: 65vh; overflow-y: auto;">
        <div v-for="twitter in this.twitterNews" >
          <Card :title="twitter.author" :bordered="false" style="width: 300px; margin-bottom: 15px; background-color:azure">
            {{ twitter.description }}
          </Card>
        </div>
      </div> 
    </Col>
  </Row>
    
</template>

<script>
export default {
  data() {
    return {
      chart: null,
      options: {
        animationEnabled: true,
        exportEnabled: true,
        title:{
          text: "Top Trending Coins in last 10 minutes."
        },
        axisX: {
          labelTextAlign: "right"
        },
        axisY: {
          title: "in Million Tonnes per Year",
          suffix: "M"
        },
        data: [{
          type: "bar",
          yValueFormatString: "#,###M tonnes",
          dataPoints: [
            { label: "Industrial Machinery", y: 3 },
            { label: "Electrical/Electronic", y: 18 },
            { label: "Transportation", y: 27 },
            { label: "Consumer & Institutional Products", y: 42 },
            { label: "Other sectors", y: 47 },
            { label: "Textiles", y: 59 },
            { label: "Building and Construction", y: 65 },
            { label: "Packaging", y: 146 }
          ]
        }]
      },

      twitterNews: [
        {author: 'manbo', description: 'how to do that #ccc'},
        {author: 'manbo', description: 'how to do that #ccc'},
        {author: 'manbo', description: 'how to do that #ccc'},
        {author: 'manbo', description: 'how to do that #ccc'},
        {author: 'manbo', description: 'how to do that #ccc'},
      ]
    }
  }
}
</script>