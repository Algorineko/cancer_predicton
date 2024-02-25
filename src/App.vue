<template>
  <div class="APP">
    <div class="headtop col-md-10 offset-md-1">
      <h1 class="text-center">Cancer Prediction</h1>
    </div>
    <div class="inputPart col-md-10 offset-md-1">
      <br>
      <div style="display: flex;">
        <!-- 上传图像 -->
        <div class="setBtn col-md-3 offset-md-2">
          <div class="alert-box-item">
            <h2 class="text-center">点击上传原图</h2>
            <div class="bigImg-div" @click="toGetImg">
              <img class="bigImg" :src=valueUrl v-if="valueUrl">
            </div>
          </div>
          <br>
          <button type="button" :disabled="!valueUrl" class="btn btn-primary col-md-5 offset-md-2" data-bs-toggle="modal" data-bs-target="#modal1">
            放大显示
          </button>
        </div>
        <!-- 显示推理图 -->
        <div class="setBtn col-md-3 offset-md-2">
          <div class="alert-box-item">
            <h2 class="text-center">显示推理图</h2>
            <div class="bigImg-div">
              <img class="bigImg" :src=outputImg v-if="outputImg">
            </div>
          </div>
          <br>
          <button type="button" :disabled="!outputImg" class="btn btn-primary col-md-5 offset-md-2" data-bs-toggle="modal" data-bs-target="#modal2">
            放大显示
          </button>
        </div>
      </div>
      <br>
      <!-- <button type="button" class="btn btn-primary col-md-6 offset-md-3" @click="handleRecognize">识 别</button> -->
      <br><br>
      <table class="table table-sm table-bordered text-center">
        <thead>
          <tr>
            <th scope="col">Predicted</th>
            <th scope="col">Confidence</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th>{{predicted}}</th>
            <td>{{confidence}}%</td>
          </tr>
        </tbody>
      </table>
      <button type="button" class="btn btn-secondary col-md-6 offset-md-3" data-bs-toggle="modal" data-bs-target="#modal3">
        相关信息
      </button>
    </div>
    <!-- 原图放大模态框 -->
    <div class="modal" tabindex="-1" id="modal1">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">原图</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <img :src=valueUrl class="img-fluid" alt="原图">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <!-- 推理图放大模态框 -->
    <div class="modal" tabindex="-1" id="modal2">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">推理图</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <img :src=outputImg class="img-fluid" alt="推理图">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <!-- 相关信息模态框 -->
    <div class="modal" tabindex="-1" id="modal3">
      <div class="modal-dialog modal-dialog-centered modal-lg ">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">相关信息</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>{{ infoContent }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import axios from 'axios';
  let inputElement = null
	export default {
		data() {
			return {
				valueUrl: '',
        outputImg:'',
        predicted: "待检测",
        confidence: 0,
        infoContent:
        `
        乳房钙化是乳房X光检查中常见的现象,它们通常是由细胞死亡后形成的钙化沉积。这些钙化点在乳房X光片上呈现为小而白的斑点,大多数情况下与良性变化相关,但在少数情况下,它们可能是乳腺癌,特别是乳腺导管内原位癌(DCIS)的早期迹象。乳腺导管内原位癌是一种非侵入性癌症,癌细胞局限于乳导管内,如果得到及时治疗,治愈率很高,但若忽视,可能会进展为更严重的侵入性乳腺癌。
        乳房钙化的形态和分布对于判断其性质至关重要。如果钙化点分布稀疏、大小不一或呈线状,通常被认为是良性的,而密集分布或形态各异的钙化则可能需要进一步的乳房活组织检查。放射学专家会根据乳房X光片的结果,结合患者的病史和之前的检查结果,来决定是否需要进行活检。
        乳房密度也是一个重要的考量因素。高乳房密度,即腺体和纤维组织占乳房组织的一半以上,可能会增加患乳腺癌的风险。放射学家在解读乳房X光片时,会评估乳房密度,并将其作为评估乳腺癌风险的一个因素。
        总之,乳房钙化是乳房健康检查中的一个重要发现,需要根据其特征和患者的具体情况进行综合评估。医生会根据乳房X光片的结果,指导患者进行必要的进一步检查和治疗,以确保及时发现并处理任何潜在的健康问题。
        `
			}
		},
		methods: {
      handleRecognize(){
      },
			toGetImg() {
				if (inputElement === null) {
				// 生成文件上传的控件
					inputElement = document.createElement('input')
					inputElement.setAttribute('type', 'file')
					inputElement.style.display = 'none'
					if (window.addEventListener) {
						inputElement.addEventListener('change', this.uploadFile, false)
					} else {
						inputElement.attachEvent('onchange', this.uploadFile)
					}
					document.body.appendChild(inputElement)
				}
				inputElement.click()
			},
			uploadFile(el) {
				if (el && el.target && el.target.files && el.target.files.length > 0) {
					const files = el.target.files[0]
					const isLt5M = files.size / 1024 / 1024 < 5
					// 判断上传文件的大小
					if (!isLt5M) {
						this.$message.error('上传图片大小需小于5MB!')
					} else if (files.type.indexOf('image') === -1) { 
						this.$message.error('请选择图片文件');
					} else {
						const that = this;
						const reader = new FileReader(); // 创建读取文件对象
						reader.readAsDataURL(el.target.files[0]); // 发起异步请求,读取文件
						reader.onload = function() { // 文件读取完成后
							// 读取完成后,将结果赋值给img的src
							that.valueUrl = this.result;
              // 使用 Axios 发送图片到后端
              const formData = new FormData();
              formData.append('image', files);
              axios.post('http://127.0.0.1:8000/recognition', formData)
              .then(response => {
                // 处理后端返回的结果
                console.log(response.data.message);
                that.predicted=response.data.Predicted;
                that.confidence=response.data.Confidence;
                that.outputImg = response.data.Output;
              })
              .catch(error => {
                console.error('上传图片错误:', error);
                if (error.response) {
                  console.log('错误相应状态:', error.response.data);
                }
              });
						};
					}
				}
			}
		},
		beforeDestroy() {
      if (inputElement) {
        if (window.addEventListener) {
          inputElement.removeEventListener('change', this.onGetLocalFile, false)
        } else {
          inputElement.detachEvent('onchange', this.onGetLocalFile)
        }
        document.body.removeChild(inputElement)
        inputElement = null
        console.log('========inputelement destroy')
      }
    }
	}
</script>
<style>
  .APP{
    background-color: #96bdeb90;
    height: 100vh;
  }
  .alert-box-item {
      overflow: hidden;
      width: 200px;
    }
	.bigImg-div {
		width: 200px;
		height: 200px;
		border-radius: 20%;
		overflow: hidden;
		border: 1px solid #00000072;
    margin: auto;
	}
	.bigImg {
		display: block;
		width: 200px;
		height: 200px;
		border-radius: 20%;
	}
  .nav_header {
    font-size: large;
    font-weight: bold;
    color: rgb(21, 3, 55);
  }
  .show_area{
    padding: 0;
  }
  .mainpart{
    padding: 5% 0px;
  }
  .headtop{
    padding-top: 100px;
  }
</style>
