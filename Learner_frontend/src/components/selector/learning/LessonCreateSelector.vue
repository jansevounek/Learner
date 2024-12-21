<template>
    <div class="selections-container">
        <!--Name section-->
        <div @click="currentIndex = 0">
            <div class="selections-item" :class="{ selected: currentIndex === 0, firstitem: true }">
                <h1 class="selections-item-content">Name</h1>
                <p class="selections-item-content">name: 
                    <input type="text" class="cmd-input" v-focus="currentIndex === 0" v-model="nameInput">
                </p>
            </div>
        </div>
        <!--other section-->
        <div @click="currentIndex = 1">
            <div class="selections-item" :class="{ selected: currentIndex === 1 }">
                <h1 class="selections-item-content">The task</h1>
                <a class="selections-item-content text-blue-600" @click="displayDetails = !displayDetails">expand 
                    <span v-if="!displayDetails || currentIndex != 1">▲</span>
                    <span v-if="displayDetails && currentIndex == 1">▼</span>
                </a>
            </div>
            <div class="selections-item-details" v-if="displayDetails && currentIndex == 1">
                <p class="text-center underline">Please input the desired task:</p>
                <textarea class="textarea-input" v-focus="displayDetails && currentIndex == 1" v-model="taskArea">
                </textarea>
            </div>
        </div>
        <div @click="currentIndex = 2">
            <div class="selections-item" :class="{ selected: currentIndex === 2 }">
                <h1 class="selections-item-content">Container settings</h1>
                <a class="selections-item-content text-blue-600" @click="displayDetails = !displayDetails">expand 
                    <span v-if="!displayDetails || currentIndex != 2">▲</span>
                    <span v-if="displayDetails && currentIndex == 2">▼</span>
                </a>
            </div>
            <div class="selections-item-details" v-if="displayDetails && currentIndex == 2">
                <div class="item-details-checkbox-container" :class="{ selected: subIndex1 === 0 }">
                    <div class="item-details-checkbox" :class="{ checboxSelected: networkSelected }" @click="networkSelected = !networkSelected"></div>
                    <label class="mr-1">Network required</label>
                </div>
                <div class="item-details-checkbox-container" :class="{ selected: subIndex1 === 1 }">
                    <div class="item-details-checkbox" :class="{ checboxSelected: sudoSelected }" @click="sudoSelected = !sudoSelected"></div>
                    <label class="mr-1">Sudo required</label>
                </div>
                <div class="item-detail-input-container" :class="{ selected: subIndex1 === 2 }">
                    <p class="mx-2">What memory load is allowed</p>
                    <input type="number" class="item-detail-input" placeholder="0-100" v-model="networkLoadInput" v-focus="displayDetails && currentIndex == 2 && subIndex1 == 2">
                </div>
                <div class="item-detail-input-container mb-3" :class="{ selected: subIndex1 === 3 }">
                    <p class="mx-2">What cpu load is allowed</p>
                    <input type="number" class="item-detail-input" placeholder="0-100" v-model="cpuLoadInput" v-focus="displayDetails && currentIndex == 2 && subIndex1 == 3">
                </div>
            </div>
        </div>
        <div @click="currentIndex = 3">
            <div class="selections-item-date" :class="{ selected: currentIndex === 3 }">
                <h1 class="selections-item-content">Time of availibility</h1>
                <p class="selections-item-content">
                    <VueDatePicker v-model="date" range multi-calendars dark/>
                </p>
            </div>
        </div>
        <div @click="currentIndex = 4">
            <div class="selections-item" :class="{ selected: currentIndex === 4 }">
                <h1 class="selections-item-content">Teams</h1>
                <a class="selections-item-content text-blue-600" @click="displayDetails = !displayDetails">expand 
                    <span v-if="!displayDetails || currentIndex != 4">▲</span>
                    <span v-if="displayDetails && currentIndex == 4">▼</span>
                </a>
            </div>
            <div class="selections-item-details" v-if="displayDetails && currentIndex == 4">
                <div class="item-details-checkbox-container" v-for="(team, index) in adminTeams" :class="{ selected: subIndex2 === index }" :ref="'item-n-' + index">
                    <div class="item-details-checkbox" :class="{ checboxSelected: teamSelected == team.id }" @click="selectTeam(team.id)"></div>
                    <label class="mr-1">{{ team.name }}</label>
                </div>
                <span class="mt-2"></span>
            </div>
        </div>
        <div @click="currentIndex = 5">
            <div class="selections-item" :class="{ selected: currentIndex === 5 }">
                <h1 class="selections-item-content">Teams</h1>
                <a class="selections-item-content text-blue-600" @click="displayDetails = !displayDetails">expand 
                    <span v-if="!displayDetails || currentIndex != 5">▲</span>
                    <span v-if="displayDetails && currentIndex == 5">▼</span>
                </a>
            </div>
            <div class="selections-item-details" v-if="displayDetails && currentIndex == 5">
                <div class="item-details-checkbox-container" :class="{ selected: subIndex3 === 0 }">
                    <div class="item-details-checkbox" :class="{ checboxSelected: networkSelected }" @click="networkSelected = !networkSelected"></div>
                    <label class="mr-1">Nano</label>
                </div>
                <div class="item-details-checkbox-container mb-3" :class="{ selected: subIndex3 === 1 }">
                    <div class="item-details-checkbox" :class="{ checboxSelected: sudoSelected }" @click="sudoSelected = !sudoSelected"></div>
                    <label class="mr-1">git</label>
                </div>
            </div>
        </div>
        <div @click="currentIndex = 6">
            <div class="selections-item" :class="{ selected: currentIndex === 6 }">
                <b class="selection-item-button" @click="createLesson">Create</b>
            </div>
        </div>
        <div>
            <div class="selections-error" v-if="isError && !firstLoad">
                <p v-if="errors.name_errors.empty" class="selection-error">1.1 A name for the lesson is required</p>
                <p v-if="errors.name_errors.invalidAscii" class="selection-error">1.2 The name can only consist of letters and numbers</p>
                <p v-if="errors.name_errors.onlySpaces" class="selection-error">1.3 The name of the lesson must be something else then spaces</p>
                <p v-if="errors.name_errors.exists" class="selection-error">1.4 The name of the lesson is already in use - change it please</p>
                <p v-if="errors.task_errors.empty" class="selection-error">2.1 A task for the lesson is required</p>
                <p v-if="errors.task_errors.short" class="selection-error text-orange-500">2.2 The task for the lesson is short</p>
                <p v-if="errors.team" class="selection-error">3. The team for which the lesson is intended must be selected</p>
                <p v-if="errors.load" class="selection-error">4. The maximum network and cpu load of the container must be set</p>
                <p v-if="errors.time.empty" class="selection-error">5.1 The time of the lesson must be set</p>
                <p v-if="errors.time.start" class="selection-error">5.2 The lesson cannot start before today</p>
                <p v-if="errors.time.end" class="selection-error">5.3 The lesson cannot end before today</p>
                <p v-if="errors.api" class="selection-error">6. {{ apiErrorMsg }}</p>
            </div>
        </div>
        <span class="mb-12"></span>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import VueDatePicker from '@vuepic/vue-datepicker';
import { getTeam, getUserExtra, getUser, getLesson } from '@/supabase/getFunctions.js'

// router import a setup
import { useRouter } from 'vue-router'
const router = useRouter()

// all the lesson information
let taskArea = ref('')
let nameInput = ref('')
let networkSelected = ref(false)
let sudoSelected = ref(false)
let networkLoadInput = ref('')
let cpuLoadInput = ref(' ')
let date = ref();
let teamSelected = ref(0);

// errors stuff
let firstLoad = true
let errors = ref({
    name_errors: {
        empty: true,
        invalidAscii: true,
        onlySpaces: true
    },
    task_errors: {
        empty: true,
        short: true
    },
    time: {
        empty: true,
        start: true,
        end: true
    },
    team: true,
    load: true,
    api: false
})
let apiErrorMsg = ref('')

// listing stuff
const listLength = 7
const subListLength1 = 4
let subListLength2 = 0
const subListLength3 = 2
const adminTeams = ref([]);
setAdminTeams()
let displayDetails = ref(false)
let currentIndex = ref(0)
let subIndex1 = ref(0)
let subIndex2 = ref(0)
let subIndex3 = ref(0)

// mounting handlers for controls
onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
})

const vFocus = {
    mounted(el, binding) {
        if (binding.value) {
            el.focus();
        }
    },
    updated(el, binding) {
        if (binding.value) {
            el.focus();
        }
    }
}

function handleKeyDown(event) {
    if (event.key === 'ArrowDown' && event.ctrlKey) {
        if (displayDetails.value && currentIndex.value == 2) {
            subIndex1.value = (subIndex1.value + 1) % subListLength1;
        }
        if (displayDetails.value && currentIndex.value == 4) {
            subIndex2.value = (subIndex2.value + 1) % subListLength2;
        }
        if (displayDetails.value && currentIndex.value == 5) {
            subIndex3.value = (subIndex3.value + 1) % subListLength3;
        }
    } else if (event.key === 'ArrowUp' && event.ctrlKey) {
        if (displayDetails.value && currentIndex.value == 2) {
            subIndex1.value = (subIndex1.value - 1 + subListLength1) % subListLength1;
        }
        if (displayDetails.value && currentIndex.value == 4) {
            subIndex2.value = (subIndex2.value - 1 + subListLength2) % subListLength2;
        }
        if (displayDetails.value && currentIndex.value == 5) {
            subIndex3.value = (subIndex3.value - 1 + subListLength3) % subListLength3;
        }
    } else if (event.key === 'ArrowDown') {
        displayDetails.value = false
        currentIndex.value = (currentIndex.value + 1) % listLength;
        updateSelection(currentIndex.value);
    } else if (event.key === 'ArrowUp') {
        displayDetails.value = false
        currentIndex.value = (currentIndex.value - 1 + listLength) % listLength;
        updateSelection(currentIndex.value);
    } else if (event.key === 'Enter' && event.ctrlKey && currentIndex.value == 2) {
        selectContainerOptions()
    } else if (event.key === 'Enter' && event.ctrlKey && currentIndex.value == 4) {
        selectTeamOptions()
    } else if (event.key === 'Enter' && event.ctrlKey && currentIndex.value == 5) {
        selectPackageOptions()
    } else if (event.key === 'Enter' && currentIndex.value == 6) {
        createLesson()
    } else if (event.key === 'Enter') {
        displayDetails.value = !displayDetails.value
    } else if (event.key === 'Escape') {
        displayDetails.value = false
    } else if (event.ctrlKey && event.key === 'c') {
        router.push('/learning/admin')
    }
}

function updateSelection(index) {
    currentIndex.value = index;
}

function selectContainerOptions() {
    if (subIndex1.value === 0) {
        networkSelected.value = !networkSelected.value
    } else if (subIndex1.value === 1) {
        sudoSelected.value = !sudoSelected.value
    }
}

function selectTeamOptions() {
    teamSelected.value = adminTeams.value[subIndex2.value].id
}

function selectPackageOptions() {
    
}

async function createLesson() {
    let error = {
        name_errors: {
            empty: true,
            invalidAscii: true,
            onlySpaces: true,
            exists: true
        },
        task_errors: {
            empty: true,
            short: true
        },
        time: {
            empty: true,
            start: true,
            end: true
        },
        team: true,
        load: true,
        api: false
    }

    error = await testName(error)

    error = testTask(error)
    
    if (networkLoadInput.value > 0 && networkLoadInput.value < 100 && cpuLoadInput.value > 0 && cpuLoadInput.value < 100) {
        error.load = false
    }

    if (date.value) {
        error.time.empty = false

        let todaysTime = new Date();
        if (date.value[0] >= todaysTime) {
            error.time.start = false
        }
        if (date.value[1] >= todaysTime) {
            error.time.end = false
        }
    }

    if (teamSelected.value != 0) {
        error.team = false
    }

    errors.value = error
    firstLoad = false

    if (!isError(error)) {
        create()
    }
}

async function testName(error) {
    if (nameInput.value != "") {
        error.name_errors.empty = false
    }
    // taken from https://bobbyhadz.com/blog/javascript-check-if-string-contains-only-letters-and-numbers#check-if-string-contains-only-letters-and-numbers-in-javascript
    if (/^[A-Za-z0-9 _]*$/.test(nameInput.value) && !nameInput.value.includes("supabase")) {
        error.name_errors.invalidAscii = false
    }

    // taken from https://stackoverflow.com/questions/10261986/how-to-detect-string-which-contains-only-spaces
    if (nameInput.value.replace(/\s/g, '').length) {
        error.name_errors.onlySpaces = false
    }

    let lesson = await getLesson({ name: nameInput.value })

    if (lesson.length == 0) {
        error.name_errors.exists = false
    }

    return error
}

function testTask(error) {
    if (taskArea.value != "" && taskArea.value.replace(/\s/g, '').length) {
        error.task_errors.empty = false
    }

    if (taskArea.value.length > 50) {
        error.task_errors.short = false
    }
    return error
}

function isError(error) {
    if (
        error.name_errors.empty ||
        error.name_errors.invalidAscii ||
        error.name_errors.onlySpaces ||
        error.load ||
        error.time.empty ||
        error.time.start ||
        error.time.end ||
        error.task_errors.empty ||
        error.task_errors.short ||
        error.api
    ) {
        return true
    }
    return false
}

function selectTeam(id) {
    teamSelected.value = id;
}

async function setAdminTeams() {
    let extra = await getUserExtra()
    adminTeams.value = await getTeam({ creator_id : extra[0].id })
    subListLength2 = adminTeams.value.length
}

async function create() {
    const user = await getUser();
    const apiurl = import.meta.env.VITE_API_URL
    const response = await fetch(apiurl + "/lessons/admin/create", {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
            user_id: user.id,
            name: nameInput.value,
            task: taskArea.value,
            container_settings: {
                network: networkSelected.value,
                sudo: sudoSelected.value,
                network_load: networkLoadInput.value,
                cpu_load: cpuLoadInput.value
            },
            date: date.value,
            team_id: teamSelected.value
        })
    })
    const data = await response.json()
    if (!data.status) {
        errors.value.api = true
        apiErrorMsg.value = data.msg
    } else {
        router.push("/learning/admin")
    }
}
</script>

<style scoped>
.dp__theme_dark {
    --dp-background-color: #000000;
    --dp-text-color: #33ff00;
    --dp-hover-color: #33ff00;
    --dp-hover-text-color: #33ff00;
    --dp-hover-icon-color: #33ff00;
    --dp-primary-color: #33ff00;
    --dp-primary-disabled-color: #33ff00;
    --dp-primary-text-color: #33ff00;
    --dp-secondary-color: #33ff00;
    --dp-border-color: #33ff00;
    --dp-menu-border-color: #33ff00;
    --dp-border-color-hover: #33ff00;
    --dp-border-color-focus: #33ff00;
    --dp-disabled-color: #33ff00;
    --dp-disabled-color-text: #33ff00;
    --dp-scroll-bar-background: #33ff00;
    --dp-scroll-bar-color: #33ff00;
    --dp-success-color: #33ff00;
    --dp-success-color-disabled: #33ff00;
    --dp-icon-color: #33ff00;
    --dp-danger-color: #33ff00;
    --dp-marker-color: #33ff00;
    --dp-tooltip-color: #33ff00;
    --dp-highlight-color: rgb(0 92 178 / 20%);
    --dp-range-between-dates-background-color: var(--dp-hover-color, #33ff00);
    --dp-range-between-dates-text-color: var(--dp-hover-text-color, #33ff00);
    --dp-range-between-border-color: var(--dp-hover-color, #33ff00);
}
</style>