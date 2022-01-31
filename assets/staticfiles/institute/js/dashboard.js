window.addEventListener("load", function(event) {
  const vm = new Vue({
    delimiters: ["[[", "]]"],
    vuetify: new Vuetify({
      theme: { dark: true },
    }),

    el: '#app',
    data: () => ({
      focus: '',
      type: 'month',
      typeToLabel: {
        month: 'Month',
        week: 'Week',
        category: 'day',
      },
      selectedEvent: {},
      selectedElement: null,
      selectedOpen: false,
      events: [],
      categories: ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th'],
      academic: {
        lecture: [
          { 'start': '07:00', 'end': '08:00', 'color': 'blue' },
          { 'start': '08:00', 'end': '09:00', 'color': 'indigo' },
          { 'start': '09:30', 'end': '10:30', 'color': 'deep-purple' },
          { 'start': '10:30', 'end': '11:30', 'color': 'grey darken-1' },
          { 'start': '12:00', 'end': '13:00', 'color': 'red' },
          { 'start': '13:00', 'end': '14:00', 'color': 'yellow' },
          { 'start': '14:30', 'end': '15:30', 'color': 'purple' },
          { 'start': '15:30', 'end': '16:30', 'color': 'black' }
        ],
        lab: [
          { 'start': '07:00', 'end': '09:00', 'color': 'cyan' },
          { 'start': '09:30', 'end': '11:30', 'color': 'green' },
          { 'start': '12:00', 'end': '14:00', 'color': 'orange' },
        ]
      },



    }),

    methods: {


      branchChange(e) {
        var ax = axiosPost('', {
          branch: e
          // branch: e.substring(0,2)
        })
        ax.then((response) => {
          response.data['Events'].forEach((item, index) => {
            console.log(this.academic)
            // console.log(this.academic[item.class_type])
            // console.log(this.academic[item.class_type][item.slot - 1])
            response.data['Events'][index]['color'] = this.academic[item.class_type][item.slot - 1]['color']
            response.data['Events'][index]['start'] = item.date + ' ' + this.academic[item.class_type][item.slot - 1]['start']
            response.data['Events'][index]['end'] = item.date + ' ' + this.academic[item.class_type][item.slot - 1]['end']
            response.data['Events'][index]['semester'] = this.categories[parseInt(item.semester) - 1]
          })
          this.events = response.data['Events']
          this.updateRange()
          console.log(this.events)

        })


      },









      viewDay({ date }) {
        this.focus = date
        this.type = 'category'
        // this.type = 'day'
      },
      getEventColor(event) {
        return event.color
      },
      setToday() {
        this.focus = ''
      },
      prev() {
        this.$refs.calendar.prev()
      },
      next() {
        this.$refs.calendar.next()
      },
      showEvent({ nativeEvent, event }) {
        const open = () => {
          this.selectedEvent = event
          this.selectedElement = nativeEvent.target
          setTimeout(() => {
            this.selectedOpen = true
          }, 10)
        }

        if (this.selectedOpen) {
          this.selectedOpen = false
          setTimeout(open, 10)
        } else {
          open()
        }

        nativeEvent.stopPropagation()
      },
      updateRange() {
        var categories = ['1st', '2nd']
        const events = []
        this.events.forEach(function (item, index) {
          events.push({
            name: item['name'],
            start: new Date(item['start']),
            end: new Date(item['end']),
            details: item['student'],
            color: item['color'],
            timed: true,
            category: item['semester'],
          })
        })

        this.events = events
      },
    },

    mounted() {
      this.$refs.calendar.checkChange()
      this.focus = 'month'
      document.getElementById('app').style.display = "block"
    },

    

  })



});