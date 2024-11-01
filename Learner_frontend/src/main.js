import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// css imports
import './styles/views/Title.css';
import './styles/navbar/NavBarTop.css';
import './styles/navbar/NavBarBottom.css';
import './styles/commandline/CommandLine.css';
import './styles/selector/Selector.css';
import './styles/containers/Containers.css';
import './styles/selector/SelectorAddon.css';

// taken from https://vue3datepicker.com/installation/
import '@vuepic/vue-datepicker/dist/main.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
