<template>
  <div class="wrapper">
    <div class="hakaton">
      <div class="left">
        <img alt="ЛЕС" src="../assets/photo.png" />
        <div class="coords">
          <div
            class="coord"
            v-for="coord in coords"
            :key="'coord_' + coord.id"
            :class="{
              selected: activeDot && activeDot.id === coord.id,
              isChoice: coord.choice !== null,
            }"
            @click="changeDot(coord)"
            :style="{
              top: coord.y + 'px',
              left: coord.x + 'px',
            }"
          >
            <div class="hint">
              <div class="name">
                {{ coord.name }}
              </div>
              <div class="owner" v-if="coord.choice !== null">
                Выбрано:
                {{ choices.filter((ch) => coord.choice === ch.id)[0].name }}
              </div>
            </div>
          </div>
        </div>

        <div class="menu">
          <div class="menu-list">
            <div class="menu-list-item" v-if="total_price > 0">
              Оставшийся бюджет: {{ total_price - selectedPrice }}
            </div>
          </div>
          <button class="btn btn-primary"
            @click="saveChanges"
            v-if="total_price > 0"
            :class="{
              disabled: total_price < selectedPrice || !choices.filter((ch) => ch.choice !== null).length
            }"
          >
            Сохранить
          </button>
        </div>
      </div>
      <div class="right">
        <div class="select_wrapper">
          <div
            class="select-item"
            v-for="ch in choices"
            :key="'choice_' + ch.id"
            @click="selectChoice(ch)"
          >
            <div class="name select-item-flex">
              <div class="title">
                Имя:
              </div>
              <div class="text">
                {{ ch.name }}
              </div>
            </div>
            <div class="price select-item-flex">
              <div class="title">
                Цена:
              </div>
              <div class="text">
                {{ ch.price }}
              </div>
            </div>
            <div class="owner select-item-flex" v-if="ch.choice !== null">
              <div class="title">
                Выбрано:
              </div>
              <div class="text">
                {{ coords.filter((cr) => cr.choice === ch.id)[0].name }}
              </div>
            </div>

            <div class="photo-wrapper popup" v-if="ch.selected === true">
              <div class="popup-body">
                <div class="close-popup" @click.stop="unselectChoices">
                  <svg
                    width="22px"
                    height="22px"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M16 8L8 16M8.00001 8L16 16"
                      stroke="#000000"
                      stroke-width="1.5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </div>
                <div class="wrapper">
                  <swiper :slides-per-view="1" :space-between="30">
                    <swiper-slide
                      v-for="(img, imageIndex) in ch.photos"
                      :key="img + imageIndex"
                    >
                      <img
                        :src="img"
                        alt="img"
                      />
                    </swiper-slide>
                  </swiper>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="error-modal" v-if="errorText && errorText.length > 0">
      {{errorText}}
    </div>
  </div>
</template>

<script>
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
export default {
  name: "HelloWorld",
  components: {
    Swiper,
    SwiperSlide,
  },
  props: {
    msg: String,
  },
  data() {
    return {
      coords: [],
      errorText: '',
      total_price: 0,
      activeDot: null,
      choices: [],
    };
  },

  created() {
    this.getData()

    this.choices = this.choices.map((item) => {
      return {
        ...item,
        choice: null,
      };
    });

    this.coords = this.coords.map((item) => {
      return {
        ...item,
        choice: null,
      };
    });
  },
  computed: {
    selectedPrice() {
      return this.choices.reduce((acc, item) => {
        if (item.choice) {
          acc += item.price;
        }

        return acc;
      }, 0);
    },
  },
  methods: {
    async getData() {
      const response = await fetch('https://b2b9-176-126-15-36.ngrok-free.app/api/survey/', {
        headers: {
          "ngrok-skip-browser-warning": "69420"
        },
      });
      if (response.ok) {
        const data = await response.json();
        this.setData(data)
      } else {
        console.log('Error:', response.status);
      }
    },

    setData(data) {
      this.coords = data.coords.map(c => {
        return {
          ...c,
          selected: false,
          choice: null,
        }
      })

      this.choices = data.choices.map(c => {
        return {
          ...c,
          selected: false,
          choice: null,
        }
      })

      this.total_price = data.total_price
    },

    setErrorText(text) {
      this.errorText = text


      setTimeout(() => {
        this.errorText = ''
      }, 2000)
    },
    unselectChoices() {
      this.choices = this.choices.map((item) => {
        return {
          ...item,
          selected: false,
        };
      });
    },

    changeDot(dot) {
      if (dot.choice !== null) {
        this.choices = this.choices.map((item) => {
          if (item.choice === dot.id) {
            return {
              ...item,
              choice: null,
            };
          }
          return item;
        });

        this.coords = this.coords.map((item) => {
          if (dot.id === item.id) {
            return {
              ...item,
              choice: null,
            };
          }

          return item;
        });

        return;
      }

      this.setActiveDot(dot);
    },

    setActiveDot(dot) {
      this.activeDot = dot;
    },

    saveChanges() {
      const selectedChoices = this.choices.filter(choice => choice.choice !== null)
      const saveChoices = selectedChoices.map(choice => {
        return {
          choice_id: choice.id, coords_id: choice.choice
        }
      })

      if (saveChoices && saveChoices.length) {
        this.saveChangesRequest({
          choices: saveChoices
        })
      } else {
        this.setErrorText('Выберите объекты')
      }
    },

    saveChangesRequest(data) {
      fetch('https://b2b9-176-126-15-36.ngrok-free.app/api/survey/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            window.location = window.location.origin + '/survey/end/'
          } else if (data.error) {
             this.setErrorText(data.error)
          } else {
            this.setErrorText('Произошла ошибка сервера, попробуйте позже или перезагрузите')
          }
        })
        .catch(() => {
          this.setErrorText('Произошла ошибка сервера, попробуйте позже или перезагрузите')
        });
    },

    selectChoice(ch) {
      if (this.activeDot !== null) {
        const oldSelectedDot = ch.choice

        if (this.selectedPrice + ch.price > this.total_price) {
          this.setErrorText('Вы вышли за рамки бюджета')
          return
        }
        this.choices = this.choices.map((item) => {
          if (ch.id === item.id) {
            return {
              ...item,
              choice: this.activeDot.id,
            };
          } else {
            return item;
          }
        });

        this.coords = this.coords.map((item) => {
          if (oldSelectedDot === item.id && oldSelectedDot !== this.activeDot.id) {
            return {
              ...item,
              choice: null,
            };
          }
          if (item.id === this.activeDot.id) {
            return {
              ...item,
              choice: ch.id,
            };
          }

          return item;
        });

        this.activeDot = null;
        return;
      }
      this.choices = this.choices.map((item) => {
        if (item.id === ch.id) {
          return {
            ...item,
            selected: true,
          };
        }
        return {
          ...item,
          selected: false,
        };
      });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.disabled {
  pointer-events: none;
  cursor: default;
  opacity: .5;
}

.error-modal {
  position: fixed;
  bottom: 32px;
  right: 32px;
  background-color: #ff6969;
  color: #fff;
  border: solid 1px #ff2b2b;
  font-size: 20px;
  padding: 10px 20px;
  border-radius: 30px;
  z-index: 100;
}
.hakaton {
  display: flex;
  align-items: center;
  margin: 0 auto;
  height: 95vh;
  overflow: auto;
  padding: 10px;
  margin: 0;
  margin-top: 0;
  outline: 0;
}

.menu {
  padding: 10px 30px;
  z-index: 3;
  background-color: #fff;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.menu-list-item {
  font-size: 18px;
}

.btn {
  margin-left: 32px;
  font-size: 20px;
  padding: 10px 20px;
  border: solid 1px blue;
  color: blue;
  background-color: #fff;
  outline: none;
  border-radius: 10px;
  cursor: pointer;


  transition: .2s ease-in-out;
}

.btn:hover {
  background-color: blue;
  color: white;
}

.popup {
  width: calc(100% - 20px);
  background: #fff;
  transition: .2s ease-in-out;
}

.popup-body {
  position: relative;
  padding-top: 32px;
}

.wrapper {
  height: 200px;
}

.wrapper .swiper {
  height: 200px;
}

.wrapper .swiper .swiper-slide img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.close-popup {
  position: absolute;
  right: 3px;
  top: 3px;
  display: flex;
  cursor: pointer;
}

.close-popup svg {
  width: 100%;
  height: 100%;
}

.modal {
  position: fixed;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
}

.modal-overlay {
  background-color: #000;
  opacity: 0.5;
  position: fixed;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
}

.modal-body {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  height: 900px;
  width: 90vw;
  background-color: #fff;
  border-radius: 16px;
}

.coord {
  position: absolute;
  width: 12px;
  height: 12px;
  border: solid 2px green;
  cursor: pointer;
  border-radius: 100%;
  transform: translate(-50%, -50%);
  transition: 0.2s ease-in-out;
  background-color: #fff;
}

.coord:hover {
  width: 18px;
  height: 18px;
}

.coord .hint {
  opacity: 1;
  visibility: visible;
  transition: 0.2s ease-in-out;
  white-space: nowrap;
  background-color: green;
  width: auto;
  color: #fff;
  font-size: 14px;
  position: absolute;
  left: 0;
  top: 16px;
  padding: 5px;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: start;
}

.coord.selected {
  background-color: blue;
  border-color: blue;
}

.coord.isChoice {
  background-color: green;
  border-color: green;
}

.coord.selected .hint {
  background-color: blue;
}

.coord.selected .isChoice {
  background-color: green;
}

.left {
  position: relative;
  height: 95vh;
}



.left img {
  width: 1500px;
  height: 605.97px;
}

.right {
  width: calc(100% - 1500px);
  min-width: 200px;
  height: 95vh;
  overflow-y: auto;
}

.select_wrapper {
  display: flex;
  flex-direction: column;
  align-items: start;
}

.select-item {
  border-bottom: #b3b3b3 1px solid;
  display: flex;
  flex-direction: column;
  align-items: start;
  padding: 10px;
  width: calc(100% - 20px);
  cursor: pointer;
  transition: 0.2s ease-in-out;
  background: #fff;
  position: relative;
}

.select-item:hover {
  background: #f4f4f4;
}

.select-item:hover .popup {
  background: #f4f4f4;
  transition: .2s ease-in-out;
}

.select-item-flex {
  display: flex;
  align-items: start;
  margin-bottom: 10px;
}

.select-item-flex:last-child {
  margin-bottom: 0;
}

.select-item-flex .title {
  margin-right: 6px;
  font-size: 18px;
}

.select-item-flex .text {
  text-align: left;
  font-weight: 600;
  font-size: 18px;
}

</style>
