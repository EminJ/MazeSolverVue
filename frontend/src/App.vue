<template>
  <div v-if="!gosterarea" class="w-full h-auto flex flex-col items-center p-10">
    <textarea v-model="postdata" class="bg-gray-200 text-2xl fo w-6/12 h-[22rem] p-2 text-center"></textarea>
    <div class="w-6/12 flex justify-end "><button @click="gonder()" class="inline-block px-4 rounded my-4 py-2 text-xl bg-orange-400 hover:bg-orange-300">Gonder</button></div>
  </div>
  <div v-if="gosterarea" class="w-full flex flex-col items-center p-10">
    <div class="w-auto inline-block rounded h-auto p-2 m-5 bg-gray-100">
    <div class="flex" v-for="(row, rowIndex) in data" :key="rowIndex">
        <div v-for="(col, colIndex) in row" :key="colIndex">
          <div v-if="col === 0" class="w-8 h-8 bg-gray-400 rounded m-1  flex justify-center items-center"></div>
          <div v-if="col === 1" class="w-8 h-8 bg-green-400 rounded m-1 flex justify-center items-center">{{ col }}</div>
          <div v-if="col === 2" class="w-8 h-8 bg-red-400 rounded m-1 flex justify-center items-center">{{ col }}</div>
          <div v-if="col === 3" class="w-8 h-8 bg-yellow-400 rounded m-1 flex justify-center items-center">{{ col }}</div>
          <div v-if="col === 'S' || col === 'E'" class="w-8 h-8 bg-gray-300 rounded m-1 flex justify-center items-center">{{ col }}</div>
        </div>
    </div>
  </div>
  <p v-if="bitti" class="text-lg text-green-500 font-bold">Labirent Çözüldü!</p>
  <div class="w-6/12 flex justify-end "><button @click="refreshPage" class="inline-block px-3 rounded my-4 py-1 bg-gray-300 hover:bg-gray-200">Geri Dön</button></div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from "axios";

const bitti = ref(false);
const postdata = ref("0000000000\n0000000000\n0000000000\n0000000000\n0000000000\n0000000000\n0000000000\n0000000000\n0000000000\n0000000000");
const gosterarea = ref(false);

function convertToMatrix(data) {
  const rows = data.split('\n');
  const matrix = [];

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i].split('');
    const newRow = [];

    for (let j = 0; j < row.length; j++) {
      if (row[j] === 'S') {
        newRow.push('S');
      } else if (row[j] === 'E') {
        newRow.push('E');
      } else {
        newRow.push(parseInt(0));
      }
    }

    matrix.push(newRow);
  }

  return matrix;
}

function refreshPage() {
    window.location.reload();
  }

const matrix = convertToMatrix(postdata.value);
const data = ref(matrix);
const gonder = async () => {
  data.value = convertToMatrix(postdata.value);

  const options = {
    method: 'POST',
    url: 'http://127.0.0.1:5000/process-data',
    headers: { 'Content-Type': 'application/json' },
    data: {
      data: postdata.value
    }
  };

  try {
    const response = await axios.request(options);
    gosterarea.value = true;
    for (let i = 0; i < response.data.length; i++) {
      const element = response.data[i];
      if (data.value[element[0]][element[1]] !== 'S' && data.value[element[0]][element[1]] !== 'E') {
        data.value[element[0]][element[1]] = 0;
      }
      if (data.value[element[0]][element[1]] == 'S') data.value[element[0]][element[1]] = 'S';
      if (data.value[element[0]][element[1]] == 'E') data.value[element[0]][element[1]] = 'E';
    }
    for (let i = 0; i < response.data.length; i++) {
      const element = response.data[i];
      // if(data.value[element[0]][element[1]] === 1) continue;
      await new Promise(resolve => setTimeout(resolve, 330));
      if (data.value[element[0]][element[1]] !== 'S' && data.value[element[0]][element[1]] !== 'E') {
        data.value[element[0]][element[1]] = element[2];
      }
      if (data.value[element[0]][element[1]] == 'S') data.value[element[0]][element[1]] = 'S';
      if (data.value[element[0]][element[1]] == 'E') data.value[element[0]][element[1]] = 'E';
    }
    bitti.value = true;
  } catch (error) {
    console.error(error);
  }
};
</script>
