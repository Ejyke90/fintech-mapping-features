import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Main documentation sidebar
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Architecture',
      items: ['architecture/overview'],
    },
    {
      type: 'category',
      label: 'Guides',
      items: ['guides/getting-started'],
    },
  ],
  
  // XML Sanitizer sidebar
  xmlSanitizerSidebar: [
    'xml-sanitizer/overview',
    {
      type: 'category',
      label: 'API Reference',
      link: {
        type: 'generated-index',
        title: 'XML Sanitizer API',
        description: 'Complete API reference for the XML Sanitizer microservice',
      },
      items: [],
    },
  ],
  
  // Mapping Generator sidebar
  mappingGeneratorSidebar: [
    'intelligent-mapping-generator/overview',
    {
      type: 'category',
      label: 'API Reference',
      link: {
        type: 'generated-index',
        title: 'Intelligent Mapping Generator API',
        description: 'Complete API reference for the Intelligent Mapping Generator microservice',
      },
      items: [],
    },
  ],
};

export default sidebars;
