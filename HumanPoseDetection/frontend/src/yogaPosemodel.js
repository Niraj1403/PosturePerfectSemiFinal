import * as tf from '@tensorflow/tfjs';

let yogaModel;

export async function loadYogaPoseModel() {
    if (!yogaModel) {  // ✅ Prevents reloading
        yogaModel = await tf.loadGraphModel('/models/yoga/yoga_model.json');
        console.log("🟢 Yoga Pose Model Loaded");
    }
}

export function getYogaModel() {
    return yogaModel;
}
