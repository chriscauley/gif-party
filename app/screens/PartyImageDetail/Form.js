import React from 'react'
import { cloneDeep } from 'lodash'
import RestHook from '@unrest/react-rest-hook'
import Form, { post } from '@unrest/react-jsonschema-form'
import classnames from 'classnames'

const withPartyImageSchema = RestHook('/api/schema/PartyImage/')

const colorCss = (selected) =>
  classnames('w-8 h-8 border m-1 rounded', {
    'border-black p-1': selected,
    'p-2': !selected,
  })

class ColorSelect extends React.Component {
  render() {
    const { options, value, onChange } = this.props
    const enumOptions = options.enumOptions.filter((option) => option.value)
    enumOptions.forEach((o) => (o.selected = o.value === value))
    return (
      <div className="flex flex-wrap">
        {enumOptions.map(({ label, value, selected }) => (
          <span
            className={colorCss(selected)}
            key={value}
            title={label}
            onClick={() => onChange(value)}
          >
            <div className="w-full h-full" style={{ background: value }}></div>
          </span>
        ))}
      </div>
    )
  }
}

const getSchema = (schema, n_frames, colors) => {
  schema = cloneDeep(schema)

  // gifs already have frame counts and so they can't have more
  if (n_frames > 1) {
    delete schema.properties.n_frames
  }

  // colors are on a gif by gif basis
  schema.properties.replace_color.enum = ['']
  schema.properties.replace_color.enumNames = ['']
  colors.forEach(([color, count]) => {
    schema.properties.replace_color.enum.push(color)
    color = color.replace('srgba', 'rgba')
    schema.properties.replace_color.enumNames.push(`${color} (${count})`)
  })

  return schema
}

const getUISchema = (schema, formData = {}) => {
  const uiSchema = {}
  const hide = (property) => (uiSchema[property] = { classNames: 'hidden' })
  if (formData.method !== 'replace_color') {
    hide('fuzz')
    hide('replace_color')
  } else if (formData.method !== 'hue_rotate') {
    hide('negate_channel')
    uiSchema['replace_color'] = { 'ui:widget': ColorSelect }
  }
  return uiSchema
}

// TODO move this to a more general place
const getInitial = (schema) => {
  const initial = {}
  Object.entries(schema.properties).forEach(([key, field]) => {
    if (field.default !== null && field.default !== undefined) {
      initial[key] = field.default
    } else if (field.enum) {
      initial[key] = field.enum[0]
    }
  })
  return initial
}

class BaseImageForm extends React.Component {
  state = {
    formData: undefined,
    error: undefined,
  }
  onChange = (formData) => this.setState({ formData })

  submit = (formData) => {
    const { sourceimage_id } = this.props
    return post('/api/PartyImage/', { ...formData, sourceimage_id })
      .catch((error) => this.setState({ error }))
      .then(this.props.onSuccess)
  }

  render() {
    const { api, n_frames, colors } = this.props
    if (api.loading) {
      return null
    }
    const schema = getSchema(api.schema, n_frames, colors, this.state.formData)
    const initial = getInitial(schema)
    return (
      <Form
        schema={schema}
        uiSchema={getUISchema(schema, this.state.formData)}
        initial={initial}
        formData={this.state.formData || initial}
        error={this.state.error}
        onChange={this.onChange}
        onSubmit={this.submit}
      />
    )
  }
}

export default withPartyImageSchema(BaseImageForm)
