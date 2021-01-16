<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn  v-on="on" block outlined>
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-title>
        <span class="headline">Add Assigment</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="assignment.name" label="Assigment Name*" />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="assignment.dueDate" label="Due Date" type="date" />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="assignment.dueTime" label="Due Time" type="time" suffix="PST" />
            </v-col>
            <v-col cols="12">
              <v-file-input
                v-model="assignment.submissions"
                accept=".zip"
                label="D2L Submission ZIP*"
                append-icon="mdi-folder"
                prepend-icon="" />
            </v-col>
            <v-col cols="6">
              <v-file-input
                v-model="assignment.solution"
                accept=".cpp"
                label="Solution Unittest*"
                append-icon="mdi-file"
                prepend-icon=""
                @change="updateName"
              />
            </v-col>
            <v-col cols="6">
              <v-file-input
                v-model="assignment.makefile"
                label="Makefile*"
                append-icon="mdi-file"
                prepend-icon="" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="assignment.solution_test_suite" label="Solution Test Suite*" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="assignment.student_test_suite" label="Student Test Suite" />
            </v-col>
            <v-col cols="12">
              <v-combobox
                label="Expected Files Names"
                chips
                multiple
                disable-lookup
                :delimiters="[',',' ',';']"
                deletable-chips
                counter
                v-model="assignment.expected_files"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false">Close</v-btn>
        <v-btn color="blue" text @click="submit">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "f-assignment",
  data: () => ({
    dialog: false,
    assignment: {
      name: undefined,
      dueDate: new Date().toLocaleDateString("en-US"),
      dueTime: '22:00',
      submissions: undefined,
      solution: undefined,
      expected_files: [],
      makefile: undefined,
      solution_test_suite: '',
      student_test_suite: ''
    }
  }),
  methods: {
    async submit() {
      try {
         await this.$store.dispatch('addAssignment', {
           assignment: {
             'name': this.assignment.name,
             'due_datetime': new Date(`${this.assignment.dueDate} ${this.assignment.dueTime}`).toISOString(),
             expected_files: this.assignment.expected_files,
             solution_test_suite: this.assignment.solution_test_suite,
             student_test_suite: this.assignment.student_test_suite
           },
           submissions: this.assignment.submissions,
           solution: this.assignment.solution,
           makefile: this.makefile
         })
        this.dialog = false
      } catch (e) {
        window.alert(e.message + ' - Are you missing a field?')
      }
    },
    updateName () {
      if (this.assignment.solution) {
        this.assignment.solution_test_suite = this.assignment.solution.name.replace('.cpp', '' )
      }
    }
  }
}
</script>
