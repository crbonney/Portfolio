

module.exports = {

  name: "thread-maker",
  description: "Returns the object to create a thread",

  threadObj: async function (channel, title, description, tag_name) {

    return {
      name: `${title}`,
      message: {content: `${description}`},
      appliedTags: [
        channel.availableTags.find((tag) => {return tag.name == tag_name}).id
      ]
    }
  }

}
